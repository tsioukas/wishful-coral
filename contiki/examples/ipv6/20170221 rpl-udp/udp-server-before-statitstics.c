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
#include "contiki-lib.h"
#include "contiki-net.h"
#include "net/ip/uip.h"
#include "net/rpl/rpl.h"

#include "net/netstack.h"
#include "dev/button-sensor.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "dev/radio-sensor.h"
#include "node-id.h"

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



#define UIP_IP_BUF   ((struct uip_ip_hdr *)&uip_buf[UIP_LLH_LEN])

#define UDP_CLIENT_PORT	8765
#define UDP_SERVER_PORT	5678

#define UDP_EXAMPLE_ID  190

static struct uip_udp_conn *server_conn;

#define MAX_NODES 15

static uint16_t SD[MAX_NODES];
static uint16_t RD[MAX_NODES];
static uint16_t SC[MAX_NODES];
static uint16_t RC[MAX_NODES];


PROCESS(udp_server_process, "UDP server process");
AUTOSTART_PROCESSES(&udp_server_process);
/*---------------------------------------------------------------------------*/


//**************************** WISHFUL BEGIN ************************************
#ifdef WISHFUL_EXTENSIONS

enum {
	IEEE802154_MACSHORTADDRESS = 55909,
	IEEE802154_PHYCURRENTCHANNEL = 51638,
	CORAL_SIGNAL_RSSI = 55600,
	IEEE802154_RPL_IMIN = 8865,
	IEEE802154_RPL_I_DOUBLE=9955,
	
	CORAL_UDP_SEND = 6671,
	CORAL_UDP_RECV = 6672,
	CORAL_ICMP_SEND = 6651,
	CORAL_ICMP_RECV = 6652,
	
	CORAL_UDP_SEND_TOTAL_SINK = 6681,
	CORAL_UDP_RECV_TOTAL_SINK = 6682,
	CORAL_ICMP_SEND_TOTAL_SINK = 6683,
	CORAL_ICMP_RECV_TOTAL_SINK = 6684,
};

int8_t rssi = 0;
uint8_t myaddress = 0;
uint8_t curChannel = 134;
uint16_t sd = 0;
uint16_t sc = 0;
uint16_t rc = 0;


//from file rpl-conf.h
extern uint8_t rpl_dio_interval_min;
extern uint8_t rpl_dio_interval_doublings;

static void *getParameter(control_hdr_t* p){
	PRINTF("Inside Get Parameter\n");
	int i = 0;
	if(p->uid == IEEE802154_MACSHORTADDRESS){
		PRINTF("Address request...\n");
		myaddress = node_id; // linkaddr_node_addr.u8[0];
		return &myaddress;
		
	}else if(p->uid == CORAL_SIGNAL_RSSI){
		 SENSORS_ACTIVATE(radio_sensor);
		 rssi = radio_sensor.value;
		 PRINTF ("Reading signal value (rssi): %d\n",rssi);
		 SENSORS_DEACTIVATE(radio_sensor);
		 return &rssi;
		 
	}else if(p->uid == IEEE802154_RPL_IMIN){
		PRINTF ("Reading RPL Imin value\n");
		return &rpl_dio_interval_min;
		
	}else if(p->uid == IEEE802154_RPL_I_DOUBLE){
		PRINTF ("Reading RPL I Double\n");
		return &rpl_dio_interval_doublings;
		
	}else if(p->uid == IEEE802154_PHYCURRENTCHANNEL){
		PRINTF ("Current channel request: %u\n",curChannel);
		return &curChannel;  //???

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

	}else if(p->uid == CORAL_UDP_SEND_TOTAL_SINK){
		printf ("Reading Total UDP sent packets from Sink\n");
		sd = 0;
		for(i=0; i<MAX_NODES; i++){
			sd = sd + SD[i];
		}
		printf("TOTAL:%d\n",sd);
		return &sd;	
	}else if(p->uid == CORAL_UDP_RECV_TOTAL_SINK){
		printf ("Reading Total UDP receive packets from Sink %d\n", RD[1]);	
		return &RD[1];  // 
			
	}else if(p->uid == CORAL_ICMP_SEND_TOTAL_SINK){
		PRINTF ("Reading Total ICMP sent packets from Sink\n");
		sc = 0;
		for(i=0; i<MAX_NODES; i++){
			sc = sc + SC[i];
		}
		return &sc;			
	}else if(p->uid == CORAL_ICMP_RECV_TOTAL_SINK){
		PRINTF ("Reading Total ICMP receive packets from Sink\n");
		rc = 0;
		for(i=0; i<MAX_NODES; i++){
			rc = rc + RC[i];
		}
		return &rc;	
			
	} else {
		PRINTF ("Error: Unknown UPI\n");	
	}return NULL;
}

static error_t setParameter(void* value, control_hdr_t* p) {
	PRINTF("Inside set Parameter\n");	
	if(p->uid == IEEE802154_RPL_IMIN){
		PRINTF("Change RPL_Imin value request...");
		memcpy(&rpl_dio_interval_min,value,sizeof(uint8_t));
		PRINTF("New value=%u\n",rpl_dio_interval_min);	
		
	} else if(p->uid == IEEE802154_PHYCURRENTCHANNEL){
		PRINTF ("Changing channel [NOT IMPLEMETED YET]\n"); //???
		//memcpy(&rpl_dio_interval_doublings, value, value);
			
	} else if(p->uid == IEEE802154_RPL_I_DOUBLE){
		PRINTF ("Change RPL I Double request...");
		memcpy(&rpl_dio_interval_doublings, value, sizeof(uint8_t));	
		PRINTF("New value=%u\n",rpl_dio_interval_doublings);
	} else {
		PRINTF ("Error: Unknown UPI\n");		
	}
	return NULL;
}

param_t IEEE802154_macShortAddress = {{IEEE802154_MACSHORTADDRESS, UINT8_T,2}, getParameter, setParameter};
param_t CORAL_signal_rssi = {{CORAL_SIGNAL_RSSI, UINT16_T,2}, getParameter, setParameter};
param_t IEEE802154_RPL_Imin = {{IEEE802154_RPL_IMIN, UINT8_T,1}, getParameter, setParameter};
param_t IEEE802154_phyCurrentChannel = {{IEEE802154_PHYCURRENTCHANNEL, UINT8_T,1}, getParameter, setParameter};

param_t CORAL_udp_send = {{CORAL_UDP_SEND, UINT16_T,2}, getParameter, setParameter};
param_t CORAL_udp_recv = {{CORAL_UDP_RECV, UINT16_T,2}, getParameter, setParameter};
param_t CORAL_icmp_send = {{CORAL_ICMP_SEND, UINT16_T,2}, getParameter, setParameter};
param_t CORAL_icmp_recv = {{CORAL_ICMP_RECV, UINT16_T,2}, getParameter, setParameter};

param_t CORAL_udp_send_total_sink = {{CORAL_UDP_SEND_TOTAL_SINK, UINT16_T,2}, getParameter, setParameter};
param_t CORAL_udp_recv_total_sink = {{CORAL_UDP_RECV_TOTAL_SINK, UINT16_T,2}, getParameter, setParameter};
param_t CORAL_icmp_send_total_sink = {{CORAL_ICMP_SEND_TOTAL_SINK, UINT16_T,2}, getParameter, setParameter};
param_t CORAL_icmp_recv_total_sink = {{CORAL_ICMP_RECV_TOTAL_SINK, UINT16_T,2}, getParameter, setParameter};
#endif
//**************************** WISHFUL END ************************************





uint16_t getfromjson(uint8_t json[], char tag[], char val[]){
   int i=0;
   int t=0;
   while(json[i]!='\0'){
      if(!strncmp((char *)(json+i),(char *)tag,2)){
         i = i+2; // jump tag
         while(json[i]==':'||json[i]=='\"') {
            i++; //jump symbols
         }
         while(json[i]!=',' && json[i]!='\"' && json[i]!='}'){   //copy val
            if(t < 6) val[t]=json[i];
            t++;
            i++;
         }
         
         val[t]='\0';
         return 1;
      }
      i++;
   }         
   return 0;
}

static void
tcpip_handler(void)
{
  char *appdata;

  if(uip_newdata()) {
    appdata = (char *)uip_appdata;
    appdata[uip_datalen()] = 0;
    PRINTF("DATA recv '%s' from ", appdata);
    PRINTF("%d",
           UIP_IP_BUF->srcipaddr.u8[sizeof(UIP_IP_BUF->srcipaddr.u8) - 1]);
    PRINTF("\n");
    
    char val[6] = "     ";
    int node = UIP_IP_BUF->srcipaddr.u8[sizeof(UIP_IP_BUF->srcipaddr.u8) - 1];

   if(getfromjson(appdata, "SD", val)){  // Get SD
      SD[node] = atoi(val);
   }
   if(getfromjson(appdata, "SC", val)){  // Get SC
      SC[node] = atoi(val);
   }
   if(getfromjson(appdata, "RC", val)){  // Get RC
      RC[node] = atoi(val);
   }
   RD[node] = RD[node] + 1; // Increase received node  
    
   SD[1] = uip_stat.udp.sent;
   RD[1] = uip_stat.udp.recv;
   SC[1] = uip_stat.icmp.sent;
   RC[1] = uip_stat.icmp.recv; 
    
	int i=0;
	for(i=1;i<MAX_NODES;i++){    
   	printf("Node:%d,SD:%d,RD:%d,SC:%d,RC:%d\n", i, SD[i],RD[i],SC[i],RC[i]); 
   }
    
   PRINTF("SSTAT-ip.drop: %d\n",uip_stat.ip.drop);
	PRINTF("SSTAT-udp.drop: %d\n",uip_stat.udp.drop);
	printf("SSTAT-udp.recv: %d\n",uip_stat.udp.recv);
	printf("SSTAT-udp.sent: %d\n",uip_stat.udp.sent);
	PRINTF("SSTAT-udp.chkerr: %d\n",uip_stat.udp.chkerr);

	PRINTF("SSTAT-icmp.drop: %d\n",uip_stat.icmp.drop);
	PRINTF("SSTAT-icmp.recv: %d\n",uip_stat.icmp.recv);
	PRINTF("SSTAT-icmp.sent: %d\n",uip_stat.icmp.sent);
	PRINTF("SSTAT-icmp.chkerr: %d\n",uip_stat.icmp.chkerr);
	PRINTF("SSTAT-icmp.chkerr: %d\n",uip_stat.icmp.typeerr);
#if SERVER_REPLY
    PRINTF("DATA sending reply\n");
    uip_ipaddr_copy(&server_conn->ripaddr, &UIP_IP_BUF->srcipaddr);
    uip_udp_packet_send(server_conn, "Reply", sizeof("Reply"));
    uip_create_unspecified(&server_conn->ripaddr);
#endif
  }
}
/*---------------------------------------------------------------------------*/
static void
print_local_addresses(void)
{
  int i;
  uint8_t state;

  PRINTF("Server IPv6 addresses: ");
  for(i = 0; i < UIP_DS6_ADDR_NB; i++) {
    state = uip_ds6_if.addr_list[i].state;
    if(state == ADDR_TENTATIVE || state == ADDR_PREFERRED) {
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
PROCESS_THREAD(udp_server_process, ev, data)
{
  uip_ipaddr_t ipaddr;
  struct uip_ds6_addr *root_if;

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
				
				param_repo_add_parameter(&CORAL_udp_send_total_sink);
				param_repo_add_parameter(&CORAL_udp_recv_total_sink);
				param_repo_add_parameter(&CORAL_icmp_send_total_sink);
				param_repo_add_parameter(&CORAL_icmp_recv_total_sink);				
        }
#endif
//**************************** WISHFUL END ************************************

  PROCESS_PAUSE();

  SENSORS_ACTIVATE(button_sensor);

  PRINTF("UDP server started. nbr:%d routes:%d\n",
         NBR_TABLE_CONF_MAX_NEIGHBORS, UIP_CONF_MAX_ROUTES);
	int i=0;
	for(i=0; i<MAX_NODES; i++){
		SD[i] = 0;
		RD[i] = 0;
		SC[i] = 0;
		RC[i] = 0;
	}

#if UIP_CONF_ROUTER
/* The choice of server address determines its 6LoPAN header compression.
 * Obviously the choice made here must also be selected in udp-client.c.
 *
 * For correct Wireshark decoding using a sniffer, add the /64 prefix to the 6LowPAN protocol preferences,
 * e.g. set Context 0 to fd00::.  At present Wireshark copies Context/128 and then overwrites it.
 * (Setting Context 0 to fd00::1111:2222:3333:4444 will report a 16 bit compressed address of fd00::1111:22ff:fe33:xxxx)
 * Note Wireshark's IPCMV6 checksum verification depends on the correct uncompressed addresses.
 */
 
#if 0
/* Mode 1 - 64 bits inline */
   uip_ip6addr(&ipaddr, UIP_DS6_DEFAULT_PREFIX, 0, 0, 0, 0, 0, 0, 1);
#elif 1
/* Mode 2 - 16 bits inline */
  uip_ip6addr(&ipaddr, UIP_DS6_DEFAULT_PREFIX, 0, 0, 0, 0, 0x00ff, 0xfe00, 1);
#else
/* Mode 3 - derived from link local (MAC) address */
  uip_ip6addr(&ipaddr, UIP_DS6_DEFAULT_PREFIX, 0, 0, 0, 0, 0, 0, 0);
  uip_ds6_set_addr_iid(&ipaddr, &uip_lladdr);
#endif

  uip_ds6_addr_add(&ipaddr, 0, ADDR_MANUAL);
  root_if = uip_ds6_addr_lookup(&ipaddr);
  if(root_if != NULL) {
    rpl_dag_t *dag;
    dag = rpl_set_root(RPL_DEFAULT_INSTANCE,(uip_ip6addr_t *)&ipaddr);
    uip_ip6addr(&ipaddr, UIP_DS6_DEFAULT_PREFIX, 0, 0, 0, 0, 0, 0, 0);
    rpl_set_prefix(dag, &ipaddr, 64);
    PRINTF("created a new RPL dag\n");
  } else {
    PRINTF("failed to create a new RPL DAG\n");
  }
#endif /* UIP_CONF_ROUTER */
  
  print_local_addresses();

  /* The data sink runs with a 100% duty cycle in order to ensure high 
     packet reception rates. */
  NETSTACK_MAC.off(1);

  server_conn = udp_new(NULL, UIP_HTONS(UDP_CLIENT_PORT), NULL);
  if(server_conn == NULL) {
    PRINTF("No UDP connection available, exiting the process!\n");
    PROCESS_EXIT();
  }
  udp_bind(server_conn, UIP_HTONS(UDP_SERVER_PORT));

  PRINTF("Created a server connection with remote address ");
  PRINT6ADDR(&server_conn->ripaddr);
  PRINTF(" local/remote port %u/%u\n", UIP_HTONS(server_conn->lport),
         UIP_HTONS(server_conn->rport));

  while(1) {
    PROCESS_YIELD();
    if(ev == tcpip_event) {
      tcpip_handler();
    } else if (ev == sensors_event && data == &button_sensor) {
      PRINTF("Initiaing global repair\n");
      rpl_repair_root(RPL_DEFAULT_INSTANCE);
    }
  }

  PROCESS_END();
}
/*---------------------------------------------------------------------------*/
