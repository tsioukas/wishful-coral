#!/usr/bin/env python3
# -*- coding: utf-8 -*-



#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# gitar gc **************************************************
"""
wishful_controller_simple.py: First implementation of WiSHFUL controller

Usage:
   wishful_controller_simple.py [options] [-q | -v]

Options:
   --logfile name      Name of the logfile
   --config configFile Config file path
   --nodes nodesFile   Config file with node info

Example:
   ./wishful_simple_local_controller -v --config ./config.yaml --nodes ./nodes.yaml

Other options:
   -h, --help          show this help message and exit
   -q, --quiet         print less text
   -v, --verbose       print more text
   --version           show version and exit
"""

import sys
import datetime
import logging
import random
from contiki_helpers.global_node_manager import *
import gevent
import yaml
import wishful_upis as upis
import json
import time
import socket
import json

#from lc import write2Serial, readFromSerial
from lc import coral_lc
from threading import Thread
import threading



__author__ = "George Violettas"
__copyright__ = "Copyright (c) 2016, University of Macedonia, Greece"
__version__ = "2.2.0"
__email__ = "georgevio@gmail.com"


#connection to Java Socket Server Status
conJSS=False



# to do: Recover after a JSS failure ???

#========= Java Socks Client ====================================================
def javaSSConnection():
	global conJSS
	global sockClient
	
	
	# JSS IP or name and port. 4 now, it is in the SAME machine
	HOST = "localhost"
	PORT = 8999
	# Connect to the port on the server provided by the caller if you wish
	server_address=(HOST, PORT)

	#reset the connection if it exists...
	try:
		if sockClient:
			sockClient.close()
	except Exception as e:
		print("sockClient closing error:"+str(e) )

	# Create a TCP/IP socket
	sockClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	
	while not conJSS:
		try:
			print ("Trying to connect to JSS: " + HOST +":" + str(PORT) )
			sockClient.connect(server_address)
			#connection is NON-Blocking. If else the program halts in sockClient.recv()
			sockClient.setblocking(0) 
			print("\n...Connected to Java Socket Server (JSS)...") 
			conJSS=True
		except:# ??? Do we need to GC to wait 4 ever for the Java Server?
			print("No Java Server, waiting 5 secs...")
			time.sleep(5)
#=== it will wait here 4 ever until Java Socks Server (JSS) is found ============

controller = wishful_controller.Controller()

log = logging.getLogger('wishful_agent.main')

#global
contiki_nodes = []


@controller.new_node_callback()
def new_node(node):
	nodes.append(node)
	print("GC: New node appeared.......... Node.id=:"+node.id)#+" ,IP="+node.IP )


@controller.node_exit_callback()
def node_exit(node, reason):
	if node in nodes:
		nPos= nodes.index(node)
		print("Node leaving index:"+str(nPos) )
		del lcList[nPos] # remove the lc object
		nodes.remove(node);
		#lcList.remove(nodes.index(node) )
	print("NodeExit : NodeID : {} Reason : {}".format(node.id, reason))

def default_callback(group, node, cmd, data):
    print("{} GC: DEFAULT CALLBACK : Group: {}, NodeName: {}, Cmd: {}, Returns: {}".format(datetime.datetime.now(),group, node.name, cmd, data))

def print_response(group, node, data):
    print("{} print_reponse : Group:{}, NodeId:{}, msg:{}".format(datetime.datetime.now(), group, node.id, data))





# upi can be just a string for get (e.g. 'IEEE802154_RPL_Imin')
# or a json {'IEEE802154_RPL_Imin':12} for set.
# get_set is 0 for get or anything for set (usually 1)
# contiki_nodes can be any VALID node number or just contiki_nodes for all
def upi_exec(getORset, nodeID, upi): #returns a JSON : {station: {'UPI" : value}}
	if(nodeID == 1000): #all nodes
		nodeID=contiki_nodes #get the array of nodes

	if (getORset == 0) : # "get_parameters"
		param="get_parameters"
		return controller.execute_upi_function("radio","get_parameters",nodeID,upi)
	else: # "set_parameters"
		param="set_parameters"
		ret=controller.execute_upi_function("radio","set_parameters",nodeID,upi)
		if (ret==0):
			return "success" #{upi:"success"}
		else:
			return "fail" #{upi:"failed"}
	
	
	
	
# print_responce could be None for no function to call
def schedule_upi_exec(time, getORset, contiki_nodes, print_responce):
	if (getORset == 0) :
		param="get_parameters"
	else: 
		param = "set_parameters"
	json={}
	exec_time = datetime.datetime.now() + datetime.timedelta(seconds=time)	

	json=controller.schedule_upi_function("radio",param,exec_time,contiki_nodes,print_responce, ['IEEE802154_phyCurrentChannel'])
	return json
	

#try to send a JSON msg to JSS	
def sendJSON2JSS(json_msg):
	json_msg=str(json_msg)+str("\n") # be careful with "Can't convert 'dict' object to str implicitly"
	msg2JSS = bytes( json_msg,'UTF-8' )
	try:	
		sockClient.sendall( msg2JSS ) 
		print ("JSON msg sent to JSS: " + json_msg )
	except Exception as e:
		print("Error sending to JSS:"+str(e) )
		print("\nJSS disappeared :-(, try to reconnect")	
		#if the connection was reset close the connection and reconnect
		#javaSSConnection() # it does not work ???
		conJSS=False
		pass


		
def main(args):

	global lcs, conJSS, contiki_nodes

	printWaitNodesMsg=True # Just to control the on screen messages...
	
	
	rpl=8 #initial value	

	
	time=1200 #20 min
	#which nodes to change the RPL Imin
	nodesMobile=[10,11,12,13,14,15,16,17,18,19,20]
	# when to change RPL Imin 
	exec_time = datetime.datetime.now() + datetime.timedelta(seconds=time)
		
			
	#control loop
	while True:
		contiki_nodes = controller.get_mac_address_list()
		
			
		if contiki_nodes: # All the following will happen ONLY if at least one node exists
			print("\nConnected nodes:", [node for node in contiki_nodes]) #too much info....
			
			
			#PERIODIC example of calling a UPI. Returns a JSON
			#def upi_exec(getORset, contiki_node, upi)
			#ret=upi_exec(0, 0,["IEEE802154_RPL_Imin"])
			#print("responce :"+str(ret[0]) )  #the 2nd part of the message is a json
			#sendJSON2JSS(ret)
			
			#Example of set UPI
			#ret = controller.execute_upi_function("radio","set_parameters",contiki_nodes,{'IEEE802154_phyCurrentChannel':12})
			#print("....{}".format(ret))


#============ Sink Mote statistics ============================================
			print("\nsink mote (1) statistics:")		
			
			#total number of udp RECEIVED by sink
			nom = upi_exec(0, 1,["CORAL_udp_recv_total_sink"]) 
			nom = json.dumps(nom)
			nom=json.loads( nom )
			try:
				nominator =  nom["1"]["CORAL_udp_recv_total_sink"] 
				print ("Total packets received in sink: "+ str (nominator) )
			except Exception as e:
				print ("nom casting problem?")
				
			#total number of udp SENT by ALL stations
			denom = upi_exec(0, 1,["CORAL_udp_send_total_sink"]) 
			#print ("CORAL_udp_send_total_sink:"+ str (nom) )
			denom= json.dumps(denom)
			denom=json.loads( denom )
			try:
				denominator =  denom["1"]["CORAL_udp_send_total_sink"] 
				print ("Total packets sent: "+str(denominator))
			except Exception as e:
				print ("denom casting problem? "+str(e) )
			
			if(nominator and denominator>0):		
				#Packet Delivery Ratio
				pdr = round( (nominator / denominator)*100 ,2) # percentage 
				timeH = datetime.datetime.now()
				print ("\nPDR with server statistics: "+str (pdr)+"%\n" )
				#write values to a file
				with open("statistics.txt", "a") as myfile:
					 myfile.write( str(timeH) +" pdr : "+str(pdr)+"\n" )
					 
#============ Sink Mote statistics =======================================

			print("\nStations Statistics Received...")
			CORAL_icmp_send=  upi_exec(0, 1000,["CORAL_icmp_send"]) 
			#print("CORAL_icmp_send:"+str(CORAL_icmp_send) )
			#sendJSON2JSS (CORAL_icmp_send)
			CORAL_icmp_recv = upi_exec(0, 1000,["CORAL_icmp_recv"]) 
			#print("CORAL_icmp_recv:"+str(CORAL_icmp_recv) )
			#sendJSON2JSS (CORAL_icmp_recv)
			CORAL_udp_send = upi_exec(0, 1000,["CORAL_udp_send"]) 
			#print ("CORAL_udp_send:"+ str (CORAL_udp_send) )
			#sendJSON2JSS (CORAL_udp_send)
			
			print
			
			sumT = 0 # Each node knows its own total_packets_send 
			# total send packets is calculated by adding ALL stations' info
			for node in contiki_nodes:
				n=str(node) # for json index
				if (CORAL_udp_send): # defence programming
					CORAL_udp_send= json.dumps(CORAL_udp_send) #just json problems with '' & ""
					CORAL_udp_send=json.loads( CORAL_udp_send )
					try:
						res = CORAL_udp_send[n]["CORAL_udp_send"] 
						#print ("send packets of node:"+n+" total:"+str(res) )
						if (res):						
							sumT=sumT+res
					except Exception as e:
						print ("CORAL_udp_send JSON problem? "+str(e) )		
			
			#use this as a denominator !!! when a station is NOT connected, the packets are dropped
			print("total packets send by all nodes:"+	str(sumT) )	
			
			if(nominator and sumT>0):		
				#Packet Delivery Ratio
				pdrC = round( (nominator / sumT)*100 ,2) # percentage 
				timeH = datetime.datetime.now()
				print ("\nPDR with STATIONS' send statistics: "+str (pdrC)+"%\n" )
				#write values to a file
				with open("statistics.txt", "a") as myfile:
					 myfile.write( str(timeH) +" PDR with STATIONS' send statistics: "+str(pdrC)+"\n" )
			
#============ RPL Imin Reading all nodes =================================			
			
			
			
			rplImin=controller.execute_upi_function("radio","get_parameters",contiki_nodes,["IEEE802154_RPL_Imin"]) 
			if(rplImin):
				for node in contiki_nodes:
					n=str(node) # for json index
					if (rplImin): # defence programming
						rplImin= json.dumps(rplImin) #just json problems with '' & ""
						rplImin=json.loads( rplImin )

						try:
							Imin = rplImin[n]["IEEE802154_RPL_Imin"] 
							if (Imin):	
								res = " Node "+n+" Imin: "+str(Imin)					
								print ( res )
								#write values to a file
								with open("statistics.txt", "a") as myfile:
									 myfile.write( str(datetime.datetime.now()) +res+"\n" )
						except Exception as e:
							print ("IEEE802154_RPL_Imin JSON problem? "+str(e) )	
									
			
				#print("rplImin:"+str(rplImin) ) # too much info
				#sendJSON2JSS(rplImin) ????????? #enable ONLY when experiment read			
				#write values to a file
				with open("statistics.txt", "a") as myfile:
					myfile.write( str( datetime.datetime.now() ) +": "+str(rplImin)+"\n" )
#============ RPL Imin Reading all nodes ==================================	
				
		
#=========== Change the RPL Imin of  Stations after time=time ======
	# be careful, there is timing problem... it crashes
	
				rplIminVal =0
				mobile_nodes= [2,3,4,5]
				static_nodes = [1,6,7,8,9,10,11,12,13,14,15]
				try: 
					f = open("rplChange.txt","r")
					for line in f:
						if ( line.startswith('min') ):
							rplIminVal = 8 #min Imin
							nodes2change = static_nodes
						else:
							if ( line.startswith('max') ):
								rplIminVal = 12 #var Imin
								nodes2change = static_nodes
					f.close()
				except Exception as e:
					print("rplChange.txt problem: "+str(e) )
					
				print("changing RPL_Imin to nodes")#+str(node) )		
				try:					
					controller.execute_upi_function("radio","set_parameters",static_nodes,{"IEEE802154_RPL_Imin":rplIminVal})
				except Exception as e:
					print("upi problem: "+str(e) ) 
						


				
			#jsonObj=controller.schedule_upi_function ("radio", "set_parameters", exec_time, nodesMobile, None, {'IEEE802154_RPL_Imin':8})
			#if (jsonObj):
				#print ("RPL Imin changed: "+str(json) )
				#sendJSON2JSS (jsonObj) # send to JSS
#=========== Change the RPL Imin of Mobile Stations after time=time ======
				
			current="" #waiting for a message from JSS
			try:
				current = sockClient.recv(1024) #waiting for the Socks Server to send something
				

				
				
				
			except Exception as e:
				pass
				#print ("sockClient: "+str(e) )	#annoying repeated message because of time-outs
		
			if current:# if a message was received from JSS
				
				data=json.loads(current.decode('utf-8') ) # Everything is sent in JSON format
				print("Incoming data:"+str(data))		
#========== the particular node(s) will come from JSS ==============				
				node=data["LC"] # specific node to sent the message to, or 1000 for all
				getORset=["getORset"]
				upi=data["UPI"]
				
				ret=upi_exec(getORset, contiki_nodes,upi)
				sendJSON2JSS(ret) #send the responce (if any) to the JSS
				
				#sending the data with a UPI
				ret=upi_exec(data)
				#return the answer to the JSS
				sendJSON2JSS(ret)
				

				
				
				
#============= UPIs ==========================================================
		#"CORAL_icmp_send",6651,"UINT16_T",2,"PARAMETER","","",">"
		#"CORAL_icmp_recv",6652,"UINT16_T",2,"PARAMETER","","",">"
		#"CORAL_udp_send",6671,"UINT16_T",2,"PARAMETER","","",">"
		#"CORAL_udp_rcv_total",6672,"UINT16_T",2,"PARAMETER","","",">"

		#"IEEE802154_phyCurrentChannel",51638,"UINT8_T",1,"PARAMETER","","",">"
		#"IEEE802154_phyTXPower",58914,"UINT8_T",1,"PARAMETER","","",">"
		#"IEEE802154_macShortAddress",55909,"UINT16_T",2,"PARAMETER","","",">"
#============= UPIs ==========================================================

		else: #if nodes
			if printWaitNodesMsg:
				print ("\nNo node yet. Probing every 5 secs...")
				printWaitNodesMsg= False # it will print the above message only once...
							
		gevent.sleep(15)

	#gevent.sleep(5)
	#javaSSConnection() 
			
	controller.stop()  
	print(("GC: {} - STOPPED".format(controller.name)))  
	

if __name__ == "__main__":
	try:
		from docopt import docopt
	except:
		print("""
		Please install docopt using:
			pip install docopt==0.6.1
		For more refer to:
		https://github.com/docopt/docopt
		""")
		raise

	args = docopt(__doc__, version=__version__)

	log_level = logging.INFO  # default
	if args['--verbose']:
		log_level = logging.DEBUG
	elif args['--quiet']:
		log_level = logging.ERROR

	logfile = None
	if args['--logfile']:
		logfile = args['--logfile']

	logging.basicConfig(filename=logfile, level=log_level,
	format='%(asctime)s - %(name)s.%(funcName)s() - %(levelname)s - %(message)s')

	log.debug(args)


	config_file_path = args['--config']
	config = None
	with open(config_file_path, 'r') as f:
		config = yaml.load(f)
	controller = GlobalNodeManager (config)
	#controller.set_default_callback(default_callback)
	controller.add_callback(upis.radio.get_parameters,print_response)
	#controller.add_callback(upis.radio.set_parameters,print_response)
	
	#controller.add_callback(upis.net.get_parameters,print_response)
	#controller.add_callback(upis.net.set_parameters,print_response)

	nodes_file_path = args['--nodes']
	with open(nodes_file_path, 'r') as f:
		node_config = yaml.load(f)

	#wait for JSS
	javaSSConnection()


	# is this necessary ??????????????????????????????/
	controller.wait_for_agents (node_config['ip_address_list'])

	
	#controller.load_config(config) #load the yaml config file
	#controller.start() #start the Global Controller (GC)
	nodes = node_config['ip_address_list']

try:
	main(args)
except KeyboardInterrupt:
	log.debug("Controller exits")
finally:
	log.debug("Exit")
	controller.stop()
