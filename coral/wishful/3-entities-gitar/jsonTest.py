#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import wishful_upis as upis
import json
import time
import socket
import json
import ast

CORAL_icmp_send={1: {'IEEE802154_RPL_Imin': 12}, 2: {'IEEE802154_RPL_Imin': 12}, 3: {'IEEE802154_RPL_Imin': 12}, 4: {'IEEE802154_RPL_Imin': 12}, 5: {'IEEE802154_RPL_Imin': 12}, 6: {'IEEE802154_RPL_Imin': 12}, 7: {'IEEE802154_RPL_Imin': 12}, 8: {'IEEE802154_RPL_Imin': 12}, 9: {'IEEE802154_RPL_Imin': 12}, 10: {'IEEE802154_RPL_Imin': 8}}

contiki_nodes= [3, 9, 5, 6, 7, 1, 2, 10, 4, 8]

sumT=0
for n in contiki_nodes:
	n=str(n)

	if (CORAL_icmp_send): # defence programming
		CORAL_icmp_send= json.dumps(CORAL_icmp_send) #just json problems with '' & ""
		CORAL_icmp_send=json.loads( CORAL_icmp_send )
		sumT = sumT + CORAL_icmp_send[n]["IEEE802154_RPL_Imin"] 
		print("sumT: "+str(sumT))
		print (		CORAL_icmp_send[n]["IEEE802154_RPL_Imin"] )	
					
					
j= {'CORAL_udp_recv_total_sink': 131}
j= json.dumps(j)
print ( j )
j=json.loads(j)
val =  j["CORAL_udp_recv_total_sink"] 
print (str(val))
#j1=json.loads ( str( j ) )

