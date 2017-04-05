/**
 * \file
 *         coral.c Main CORAL mote source code
 * \author
 *         Tryfon Theodorou <tryfonthe@gmail.com>
 */
 
#include "coral.h"

#define MESSAGE "Hello"

/*---------------------------------------------------------------------------*/
PROCESS(main_coral_process, "CORAL Main Process");
AUTOSTART_PROCESSES(&main_coral_process);
/*---------------------------------------------------------------------------*/

#ifdef WISHFUL_EXTENSIONS

enum {
        IEEE802154_MACSHORTADDRESS = 55909,
};


static void* getParameter(control_hdr_t* p){
        if(p->uid == IEEE802154_MACSHORTADDRESS){
                return 1;
        }
        return NULL;
}

static error_t setParameter(void* value, control_hdr_t* p) {
	return NULL;
}

param_t IEEE802154_macShortAddress = {{IEEE802154_MACSHORTADDRESS, UINT16_T,2}, getParameter, setParameter};
#endif

static uint8_t uart_buffer[UART_BUFFER_SIZE];
static uint8_t uart_buffer_index = 0;

// Connection structs
static struct broadcast_conn bc;
static struct unicast_conn uc;
static struct mesh_conn mc;

/*============================================================================*/
/* UART CALLBACK */
int uart_rx_callback(unsigned char c){
   if(c != '\n' && uart_buffer_index < UART_BUFFER_SIZE){
      uart_buffer[uart_buffer_index++] = c;
   }
   else{
      uart_buffer[uart_buffer_index] = '\0';
      uart_buffer_index = 0;
      PRINTF("Received from UART: %s\n",uart_buffer);  
      
      char buf[3];    
      linkaddr_t dest;
      linkaddr_t nexthop;
                       
      if(!strncmp((char *)uart_buffer,"TD",2)){  // NETWORK DISCOVERY
         packetbuf_copyfrom("0", 1); // 0 = Topology discovery
         PRINTF("Sending Topology Discovey Broadcast Request message...\n"); 
         broadcast_send(&bc);   
      } 
      else if(!strncmp((char *)uart_buffer,"AD",2)||!strncmp((char *)uart_buffer,"AR",2)){    // ADD ROUTE      
         strncpy(buf,(char *)uart_buffer+2,2 );
         dest.u8[0] =  atoi(buf); // Destination net addr
         strncpy(buf,(char *)uart_buffer+4,2 );
         dest.u8[1] =  atoi(buf); // Destination host addr              
         strncpy(buf,(char *)uart_buffer+6,2 );
         nexthop.u8[0] =  atoi(buf);  // Next Hop net addr
         strncpy(buf,(char *)uart_buffer+8,2 );
         nexthop.u8[1] =  atoi(buf);  // Next Hop host addr        
         strncpy(buf,(char *)uart_buffer+10,2 ); // Cost
         uint8_t cost = atoi(buf);
         strncpy(buf,(char *)uart_buffer+12,2 ); // Sequence
         uint8_t seqno = atoi(buf);
         
         PRINTF("ADD route with destination: %u.%u via %u.%u with cost %u and sequence %u\n",
	         dest.u8[0], dest.u8[1], nexthop.u8[0],nexthop.u8[1],cost,seqno);

         route_add(&dest, &nexthop, cost, seqno);  //ADddddhhhhccss  dddd=destination, hhhh=nethop hop, cc=cost, ss=sequenceno
         if(!strncmp((char *)uart_buffer,"AR",2)){  // If received route replay stop the wating timer and resend the message
            data_packet_resend(&mc);  //mesh.c
         }
      }
      else if(!strncmp((char *)uart_buffer,"RM",2)){   // REMOVE ROUTE
         if(!strncmp((char *)uart_buffer+2,"0000",4)){  //RM0000 REMOVE ALL routing table records
            route_flush_all();
            PRINTF("REMOVING all routing records...\n"); 
         }
         else{   // REMOVE ONE 
            struct route_entry *rt;
            strncpy(buf,(char *)uart_buffer+2,2 );
            dest.u8[0] =  atoi(buf); // Destination net addr
            strncpy(buf,(char *)uart_buffer+4,2 );
            dest.u8[1] =  atoi(buf); // Destination host addr              
            rt = route_lookup(&dest);   // SEARCH in routing table
            if(rt != NULL) {
               PRINTF("REMOVING route to %u.%u \n", dest.u8[0], dest.u8[1]); 
               route_remove(rt);     // REMOVE from routing table   RMddddd  dddd=destination,
            } 
            else {
               PRINTF("Cannot remove route to %u.%u does not exists\n", dest.u8[0], dest.u8[1]); 
	         } 
	      }           
      }
      else {
         PRINTF("Unknown command from cotroller %s",uart_buffer);
      }
   }
   return 0;
}

/*============================================================================*/
/* BROADCAST CALLBACK */
static void recv_bc_callback(struct broadcast_conn *c, const linkaddr_t *from){
   PRINTF("Received from %d.%d broadcast packet: '%s' with RSSI:%u\n",
         from->u8[0], from->u8[1], (char *)packetbuf_dataptr(), 
         (uint8_t) (- packetbuf_attr(PACKETBUF_ATTR_RSSI)));
   if(!strcmp((char *)packetbuf_dataptr(),"0")){   // 0 = Topology Discovery 
      char rssi[5];
      sprintf(rssi,"%u",(uint8_t) (- packetbuf_attr(PACKETBUF_ATTR_RSSI)));
      packetbuf_copyfrom(rssi, sizeof(rssi)); // add rssi to payload
      unicast_send(&uc,from);   // SEND UNICAST Topology discovery RESPONCE   
   }
}
/*----------------------------------------------------------------------------*/
static const struct broadcast_callbacks broadcast_callbacks = { recv_bc_callback };
/*----------------------------------------------------------------------------*/

/*============================================================================*/
/* UNICAST CALLBACK */
static void recv_uc_callback(struct unicast_conn *c, const linkaddr_t *from){
   printf("Nid:%d.%d,RSSI_R:%u,RSSI_S:%s\n", from->u8[0], from->u8[1],
          (uint8_t) (- packetbuf_attr(PACKETBUF_ATTR_RSSI)),
          (char *)packetbuf_dataptr());  // PRINT TO UART (Send message to controler)
}
/*----------------------------------------------------------------------------*/
static const struct unicast_callbacks unicast_callbacks = { recv_uc_callback };
/*----------------------------------------------------------------------------*/

/*============================================================================*/
/* MESH CALLBACK */
static void sent(struct mesh_conn *c){
  PRINTF("packet sent\n");
}

static void timedout(struct mesh_conn *c){
  PRINTF("packet timedout\n");
}

static void recv(struct mesh_conn *c, const linkaddr_t *from, uint8_t hops){
  PRINTF("Data received from %d.%d: %.*s (%d)\n",
         from->u8[0], from->u8[1],
         packetbuf_datalen(), (char *)packetbuf_dataptr(), packetbuf_datalen());

  //packetbuf_copyfrom(MESSAGE, strlen(MESSAGE));
  //mesh_send(&mc, from);   // send ack
}
/*----------------------------------------------------------------------------*/
const static struct mesh_callbacks callbacks = {recv, sent, timedout};
/*----------------------------------------------------------------------------*/

/*============================================================================*/
/* MAIN PROCESS */
PROCESS_THREAD(main_coral_process, ev, data){
   PROCESS_EXITHANDLER(unicast_close(&uc);broadcast_close(&bc);mesh_close(&mc);)

   PROCESS_BEGIN();

#ifdef WISHFUL_EXTENSIONS
        if(data == NULL){
                //process_start(&uart_process, NULL);
                param_repo_add_parameter(&IEEE802154_macShortAddress);
        }
#endif




   PRINTF("Initializing route table...\n");
   route_init();
   PRINTF("Starting Broadcast listener...\n");
   broadcast_open(&bc, BC_CHANNEL, &broadcast_callbacks);   
   PRINTF("Starting Unicast listener...\n");
   unicast_open(&uc, UC_CHANNEL, &unicast_callbacks);  
   PRINTF("Starting MESH listener...\n"); 
   mesh_open(&mc, 132, &callbacks);
   PRINTF("Starting UART listener...\n"); 
#ifdef Z1  // For Z1-> uart0 
   uart0_init(BAUD2UBR(115200));       /* set the baud rate as necessary */
   uart0_set_input(uart_rx_callback);  /* set the callback function */
#elif defined SKY // For sky->uart1
   //uart1_init(BAUD2UBR(115200));       /* set the baud rate as necessary */
   //uart1_set_input(uart_rx_callback);  /* set the callback function */
#endif
   
   PRINTF("\nCORAL Main process event...\n");    

   SENSORS_ACTIVATE(button_sensor);

   static int count=0;
   char message[10];
   while(1) {
      linkaddr_t addr;

      /* Wait for button click before sending the first message. */
      PROCESS_WAIT_EVENT_UNTIL(ev == sensors_event && data == &button_sensor);

      printf("Button clicked\n");
      count++;
      /* Send a message to node number 1. */
      sprintf(message,"%s %d",MESSAGE,count);
      packetbuf_copyfrom(message, strlen(message));
//      packetbuf_copyfrom(MESSAGE, strlen(MESSAGE));
      addr.u8[0] = 1;
      addr.u8[1] = 0;
      mesh_send(&mc, &addr);
   }

   PROCESS_END();
}
/*----------------------------------------------------------------------------*/

