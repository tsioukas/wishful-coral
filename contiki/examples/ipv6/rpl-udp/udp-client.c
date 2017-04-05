/*
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. Neither the name of the Institute nor the names of its contributors
 *    may be used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE INSTITUTE AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE INSTITUTE OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 *
 * This file is part of the Contiki operating system.
 *
 */

#include "contiki.h"
#include "lib/random.h"
#include "sys/ctimer.h"
#include "net/ip/uip.h"
#include "net/ipv6/uip-ds6.h"
#include "net/ip/uip-udp-packet.h"


#ifdef WITH_COMPOWER
#include "powertrace.h"
#endif
#include <stdio.h>
#include <string.h>

/* Only for TMOTE Sky? */
#include "dev/serial-line.h"
#include "dev/uart1.h"
#include "net/ipv6/uip-ds6-route.h"
#include "dev/radio-sensor.h"
#include "node-id.h"

#define UDP_CLIENT_PORT 8765
#define UDP_SERVER_PORT 5678

#define UDP_EXAMPLE_ID  190

#ifdef WISHFUL_EXTENSIONS
        #include "../apps/param-repo/param-repo.h"
#endif

#include "net/ip/uip-debug.h"
#define DEBUG 0
#if DEBUG 
   #define PRINTF(...) printf(__VA_ARGS__)
#else
   #define PRINTF(...)
#endif

//trying to sync the time of ALL motes
//#include "sys/rtimer.h"

#ifndef PERIOD
#define PERIOD 60
#endif

#define START_INTERVAL		(15 * CLOCK_SECOND)
#define SEND_INTERVAL		(PERIOD * CLOCK_SECOND)
#define SEND_TIME		(random_rand() % (SEND_INTERVAL))
#define MAX_PAYLOAD_LEN		50

static struct uip_udp_conn *client_conn;
static uip_ipaddr_t server_ipaddr;

/*---------------------------------------------------------------------------*/
PROCESS(udp_client_process, "UDP client process");
AUTOSTART_PROCESSES(&udp_client_process);
/*---------------------------------------------------------------------------*/

static int seq_id;
static int reply;



//Number of ticks per second, for current architecture
rtimer_clock_t rtimer_secs = RTIMER_ARCH_SECOND;


//**************************** WISHFUL BEGIN ************************************
#ifdef WISHFUL_EXTENSIONS

enum {
	IEEE802154_MACSHORTADDRESS = 55909,
	IEEE802154_PHYCURRENTCHANNEL = 51638,
	IEEE802154_RPL_IMIN = 8865,
	IEEE802154_RPL_I_DOUBLE=9955,
	CORAL_SIGNAL_RSSI = 55600,
	CORAL_UDP_SEND = 6671,
	CORAL_UDP_RECV = 6672,
	CORAL_ICMP_SEND = 6651,
	CORAL_ICMP_RECV = 6652,
	CORAL_SEND_INTERVAL = 6685,
	
};

int8_t rssi = 0;
uint8_t myaddress = 0;
uint8_t curChannel = 134; //???

//multiplicator of UDP sending frequency 
uint8_t send_interval_times = 1;
uint16_t new_SEND_INTERVAL = SEND_INTERVAL;


//from file rpl-conf.h
extern uint8_t rpl_dio_interval_min;
extern uint8_t rpl_dio_interval_doublings;


static void *getParameter(control_hdr_t* p){
	//PRINTF("Inside Get Parameter\n");
	if(p->uid == IEEE802154_MACSHORTADDRESS){
		PRINTF("Address request...\n");
		myaddress = node_id; // linkaddr_node_addr.u8[0];
		return &myaddress;
		 
	}else if(p->uid == IEEE802154_RPL_IMIN){
		PRINTF ("Reading RPL Imin value\n");
		return &rpl_dio_interval_min;
		
	}else if(p->uid == IEEE802154_RPL_I_DOUBLE){
		PRINTF ("Reading RPL I Double\n");
		return &rpl_dio_interval_doublings;
		
	}else if(p->uid == IEEE802154_PHYCURRENTCHANNEL){
		PRINTF ("Current channel request: %u\n",curChannel);
		return &curChannel;  
		
	}else if(p->uid == CORAL_SIGNAL_RSSI){
		 SENSORS_ACTIVATE(radio_sensor);
		 rssi = radio_sensor.value;
		 PRINTF ("Reading signal value (rssi): %d\n",rssi);
		 SENSORS_DEACTIVATE(radio_sensor);
		 return &rssi;
		 
	}else if(p->uid == CORAL_UDP_SEND){
		PRINTF ("Reading UDP sent packets\n");
		return &uip_stat.udp.sent;	
	}else if(p->uid == CORAL_UDP_RECV){
		PRINTF ("Reading UDP receive packets\n");
		return &uip_stat.udp.recv;  
			
	}else if(p->uid == CORAL_ICMP_SEND){
		PRINTF ("Reading ICMP sent packets\n");
		return &uip_stat.icmp.sent;	
		
	}else if(p->uid == CORAL_ICMP_RECV){
		PRINTF ("Reading ICMP receive packets\n");
		return &uip_stat.icmp.recv;             
	}else if(p->uid == CORAL_SEND_INTERVAL){
		PRINTF ("Reading send_interval_times\n");
		return &send_interval_times;   
	
	
	} else {
		PRINTF ("Error: Unknown UPI\n");	
	}return NULL;
}


// be careful: VALUE does not print correct !!!!!!!!
static error_t setParameter(void* value, control_hdr_t* p) {
	PRINTF("Inside set Parameter\n");	
	if(p->uid == IEEE802154_RPL_IMIN){
		PRINTF("Change RPL_Imin value request...\n");
		memcpy(&rpl_dio_interval_min,value,sizeof(uint8_t));
		
	} else if(p->uid == IEEE802154_PHYCURRENTCHANNEL){
		PRINTF ("Changing channel [NOT IMPLEMETED YET]\n"); //???
		//memcpy(&rpl_dio_interval_doublings, value, value);
			
	} else if(p->uid == IEEE802154_RPL_I_DOUBLE){
		PRINTF ("Change RPL I Double request...\n");
		memcpy(&rpl_dio_interval_doublings, value, sizeof(uint8_t));	

	} else if(p->uid == CORAL_SEND_INTERVAL){
		printf ("Change send_interval_times request...\n");
		memcpy(&send_interval_times, value, sizeof(uint8_t));
		printf ("Original SEND_INTERVAL: %u\n", SEND_INTERVAL);

		new_SEND_INTERVAL = (uint16_t) (SEND_INTERVAL / send_interval_times);
		printf ("NEW SEND_INTERVAL: %u\n", new_SEND_INTERVAL);
		
		
	} else {
		PRINTF ("Error: Unknown UPI\n");		
	}
	return NULL;
}

param_t IEEE802154_macShortAddress = {{IEEE802154_MACSHORTADDRESS, UINT8_T,1}, getParameter, setParameter};
param_t IEEE802154_RPL_Imin = {{IEEE802154_RPL_IMIN, UINT8_T,1}, getParameter, setParameter};
param_t IEEE802154_phyCurrentChannel = {{IEEE802154_PHYCURRENTCHANNEL, UINT8_T,1}, getParameter, setParameter};

param_t CORAL_signal_rssi = {{CORAL_SIGNAL_RSSI, UINT16_T,2}, getParameter, setParameter};
param_t CORAL_udp_send = {{CORAL_UDP_SEND, UINT16_T,2}, getParameter, setParameter};
param_t CORAL_udp_recv = {{CORAL_UDP_RECV, UINT16_T,2}, getParameter, setParameter};
param_t CORAL_icmp_send = {{CORAL_ICMP_SEND, UINT16_T,2}, getParameter, setParameter};
param_t CORAL_icmp_recv = {{CORAL_ICMP_RECV, UINT16_T,2}, getParameter, setParameter};

param_t CORAL_send_interval = {{CORAL_SEND_INTERVAL, UINT8_T,1}, getParameter, setParameter};

#endif
//**************************** WISHFUL END ************************************


static void
tcpip_handler(void)
{
  char *str;

  if(uip_newdata()) {
    str = uip_appdata;
    str[uip_datalen()] = '\0';
    reply++;
    PRINTF("DATA recv '%s' (s:%d, r:%d)\n", str, seq_id, reply);
  }
}
/*---------------------------------------------------------------------------*/
static void
send_packet(void *ptr)
{
  char buf[MAX_PAYLOAD_LEN];
	
#ifdef SERVER_REPLY
  uint8_t num_used = 0;
  uip_ds6_nbr_t *nbr;

  nbr = nbr_table_head(ds6_neighbors);
  while(nbr != NULL) {
    nbr = nbr_table_next(ds6_neighbors, nbr);
    num_used++;
  }

  if(seq_id > 0) {
    ANNOTATE("#A r=%d/%d,color=%s,n=%d %d\n", reply, seq_id,
             reply == seq_id ? "GREEN" : "RED", uip_ds6_route_num_routes(), num_used);
  }
#endif /* SERVER_REPLY */



  seq_id++;

  PRINTF("DATA send to %d 'Hello %d'\n",
         server_ipaddr.u8[sizeof(server_ipaddr.u8) - 1], seq_id);
  PRINTF("STAT-ip.drop: %d\n",uip_stat.ip.drop);
  PRINTF("STAT-udp.drop: %d\n",uip_stat.udp.drop);
  PRINTF("STAT-udp.recv: %d\n",uip_stat.udp.recv);
  PRINTF("STAT-udp.sent: %d\n",uip_stat.udp.sent);
  PRINTF("STAT-udp.chkerr: %d\n",uip_stat.udp.chkerr);
  
  PRINTF("STAT-icmp.drop: %d\n",uip_stat.icmp.drop);
  PRINTF("STAT-icmp.recv: %d\n",uip_stat.icmp.recv);
  PRINTF("STAT-icmp.sent: %d\n",uip_stat.icmp.sent);
  PRINTF("STAT-icmp.chkerr: %d\n",uip_stat.icmp.chkerr);
  PRINTF("STAT-icmp.chkerr: %d\n",uip_stat.icmp.typeerr);
  

	//rtimer_clock_t tim = timesynch_time(); // THIS IS NOT WORKING !!!
	//rtimer_clock_t ticks_now = RTIMER_NOW(); // not used. using architecture spec time

	//uint32_t rtimer_arch_specific = rtimer_arch_now();
	//printf("station arch specific timer %lu\n",rtimer_arch_specific);


	// in case rtimer was reset, clock_time will be +1
	//uint32_t time_2_send =  clock_time()+  rtimer_arch_now(); 
	//printf("Node: time + real_time: %lu\n",time_2_send );	
	

	// calculate  a precise elapsed time
	//int32_t interval = RTIMER_NOW()-start;
	//if((interval < 0) interval = - intercal; // trip wraparound
	//printf("interval %u milliseconds\n",interval*RTIMER_ARCH_SECOND/1000); 
  		
  		
  		
  		
  		
	// from clock_time --> rtime : RTIMER_ARCH_SECOND / CLOCK_SECOND
	uint32_t transformer = RTIMER_ARCH_SECOND / CLOCK_SECOND;
	
	
	// time + accurate time
	uint32_t time_2_send = clock_time()*transformer + rtimer_arch_now();
   
    
	sprintf(buf, "{\"SD\":%u,\"SC\":%u,\"RC\":%u,\"TT\":%lu}", 
             uip_stat.udp.sent+1, uip_stat.icmp.sent, uip_stat.icmp.recv

				,time_2_send 


             //,rtimer_arch_specific // to be used for latency calc             
             );
  
  
  PRINTF("Sending message every: [%u]\n",new_SEND_INTERVAL);
  
  PRINTF("Sending ... %s\n", buf);
  uip_udp_packet_sendto(client_conn, buf, strlen(buf),
                        &server_ipaddr, UIP_HTONS(UDP_SERVER_PORT));
}
/*---------------------------------------------------------------------------*/


static void
print_local_addresses(void)
{
  int i;
  uint8_t state;

  PRINTF("Client IPv6 addresses: ");
  for(i = 0; i < UIP_DS6_ADDR_NB; i++) {
    state = uip_ds6_if.addr_list[i].state;
    if(uip_ds6_if.addr_list[i].isused &&
       (state == ADDR_TENTATIVE || state == ADDR_PREFERRED)) {
      PRINT6ADDR(&uip_ds6_if.addr_list[i].ipaddr);
      PRINTF("\n");
      /* hack to make address "final" */
      if (state == ADDR_TENTATIVE) {
	uip_ds6_if.addr_list[i].state = ADDR_PREFERRED;
      }
    }
  }
}
/*---------------------------------------------------------------------------*/
static void
set_global_address(void)
{
  uip_ipaddr_t ipaddr;

  uip_ip6addr(&ipaddr, UIP_DS6_DEFAULT_PREFIX, 0, 0, 0, 0, 0, 0, 0);
  uip_ds6_set_addr_iid(&ipaddr, &uip_lladdr);
  uip_ds6_addr_add(&ipaddr, 0, ADDR_AUTOCONF);

/* The choice of server address determines its 6LoPAN header compression.
 * (Our address will be compressed Mode 3 since it is derived from our link-local address)
 * Obviously the choice made here must also be selected in udp-server.c.
 *
 * For correct Wireshark decoding using a sniffer, add the /64 prefix to the 6LowPAN protocol preferences,
 * e.g. set Context 0 to fd00::.  At present Wireshark copies Context/128 and then overwrites it.
 * (Setting Context 0 to fd00::1111:2222:3333:4444 will report a 16 bit compressed address of fd00::1111:22ff:fe33:xxxx)
 *
 * Note the IPCMV6 checksum verification depends on the correct uncompressed addresses.
 */
 
#if 0
/* Mode 1 - 64 bits inline */
   uip_ip6addr(&server_ipaddr, UIP_DS6_DEFAULT_PREFIX, 0, 0, 0, 0, 0, 0, 1);
#elif 1
/* Mode 2 - 16 bits inline */
  uip_ip6addr(&server_ipaddr, UIP_DS6_DEFAULT_PREFIX, 0, 0, 0, 0, 0x00ff, 0xfe00, 1);
#else
/* Mode 3 - derived from server link-local (MAC) address */
  uip_ip6addr(&server_ipaddr, UIP_DS6_DEFAULT_PREFIX, 0, 0, 0, 0x0250, 0xc2ff, 0xfea8, 0xcd1a); //redbee-econotag
#endif
}
/*---------------------------------------------------------------------------*/
PROCESS_THREAD(udp_client_process, ev, data)
{
  static struct etimer periodic;
  static struct ctimer backoff_timer;
#if WITH_COMPOWER
  static int print = 0;
#endif

  PROCESS_BEGIN();


//**************************** WISHFUL BEGIN **********************************
#ifdef WISHFUL_EXTENSIONS
        if(data == NULL){
        		PRINTF("Wishful Extensions ON\n");
				//process_start(&uart_process, NULL);
				param_repo_add_parameter(&IEEE802154_macShortAddress);
				param_repo_add_parameter(&CORAL_signal_rssi);
				param_repo_add_parameter(&IEEE802154_RPL_Imin);
				param_repo_add_parameter(&IEEE802154_phyCurrentChannel);
				
				param_repo_add_parameter(&CORAL_udp_send);
				param_repo_add_parameter(&CORAL_udp_recv);
				param_repo_add_parameter(&CORAL_icmp_send);
				param_repo_add_parameter(&CORAL_icmp_recv);
				param_repo_add_parameter(&CORAL_send_interval);
        }
#endif
//**************************** WISHFUL END ************************************


	//trying to initialize REAL TIMER rtimer
	rtimer_init();
	rtimer_arch_init();



	//forces cooja to run in REAL TIME!
  //clock_init(); 

  


  PROCESS_PAUSE();




  set_global_address();

  PRINTF("UDP client process started nbr:%d routes:%d\n",
         NBR_TABLE_CONF_MAX_NEIGHBORS, UIP_CONF_MAX_ROUTES);

  print_local_addresses();

  /* new connection with remote host */
  client_conn = udp_new(NULL, UIP_HTONS(UDP_SERVER_PORT), NULL); 
  if(client_conn == NULL) {
    PRINTF("No UDP connection available, exiting the process!\n");
    PROCESS_EXIT();
  }
  udp_bind(client_conn, UIP_HTONS(UDP_CLIENT_PORT)); 

  PRINTF("Created a connection with the server ");
  PRINT6ADDR(&client_conn->ripaddr);
  PRINTF(" local/remote port %u/%u\n",
	UIP_HTONS(client_conn->lport), UIP_HTONS(client_conn->rport));

  /* initialize serial line */
  uart1_set_input(serial_line_input_byte);
  serial_line_init();


#if WITH_COMPOWER
  powertrace_sniff(POWERTRACE_ON);
#endif



 
  //etimer_set(&periodic, SEND_INTERVAL );
  
  
  
  

  	//trying to utilize the foloowing
	// void etimer_reset_with_new_interval(struct etimer *et, clock_time_t interval);
  
  //now we can change the sending time. it starts with the value of SEND_INTERVAL
  
  
  
  
  
  etimer_set(&periodic, new_SEND_INTERVAL); // is this working ???????
  
  
  


  while(1) {
    PROCESS_YIELD();
    if(ev == tcpip_event) {
      tcpip_handler();
    }

    if(ev == serial_line_event_message && data != NULL) {
      char *str;
      str = data;
      if(str[0] == 'r') {
        uip_ds6_route_t *r;
        uip_ipaddr_t *nexthop;
        uip_ds6_defrt_t *defrt;
        uip_ipaddr_t *ipaddr;
        defrt = NULL;
        if((ipaddr = uip_ds6_defrt_choose()) != NULL) {
          defrt = uip_ds6_defrt_lookup(ipaddr);
        }
        if(defrt != NULL) {
          PRINTF("DefRT: :: -> %02d", defrt->ipaddr.u8[15]);
          PRINTF(" lt:%lu inf:%d\n", stimer_remaining(&defrt->lifetime),
                 defrt->isinfinite);
        } else {
          PRINTF("DefRT: :: -> NULL\n");
        }

        for(r = uip_ds6_route_head();
            r != NULL;
            r = uip_ds6_route_next(r)) {
          nexthop = uip_ds6_route_nexthop(r);
          PRINTF("Route: %02d -> %02d", r->ipaddr.u8[15], nexthop->u8[15]);
          /* PRINT6ADDR(&r->ipaddr); */
          /* PRINTF(" -> "); */
          /* PRINT6ADDR(nexthop); */
          PRINTF(" lt:%lu\n", r->state.lifetime);

        }
      }
    }

    if(etimer_expired(&periodic)) {
      
      
      // original
      etimer_reset(&periodic);
      

		//trying to send more messages
		//etimer_reset_with_new_interval(&periodic, new_SEND_INTERVAL);

      
      
      //ORIGINAL
      //ctimer_set(&backoff_timer, SEND_INTERVAL, send_packet, NULL);

      
      
      
      
      //sending packets with new frequency set with UPI
      ctimer_set(&backoff_timer, new_SEND_INTERVAL, send_packet, NULL);
     	



		#if WITH_COMPOWER
			if (print == 0) {
				powertrace_print("#P");
			}
			if (++print == 3) {
				print = 0;
			}
		#endif

    }
  }

  PROCESS_END();
}
/*---------------------------------------------------------------------------*/
