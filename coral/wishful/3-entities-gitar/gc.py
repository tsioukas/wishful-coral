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
from json import JSONDecoder

#from lc import write2Serial, readFromSerial
from lc import coral_lc
from threading import Thread
import threading

from multiprocessing import Process, Queue


#import sockClientThread #  my implementation of socks client with threads

__author__ = "George Violettas"
__copyright__ = "Copyright (c) 2016, University of Macedonia, Greece"
__version__ = "2.2.0"
__email__ = "georgevio@gmail.com"


controller = wishful_controller.Controller()

log = logging.getLogger('wishful_agent.main')

#GLOBAL VARS
contiki_nodes = []			  
total_packets_recvd_sink = 0
conJSS = False 
sockClient =""	
coralLogFile = ""
FiveMinlogName = "" #log file for 5 minutes segments
logFile4PDR = "" #log file for PDR & any changes (e.g. udp send freq)
connection ="" #sockClient connection


latency_diff = []
packets_received = []
current_jitter = []
oldLatency = []
	

#JUST DEBUGGING
block=""

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

	global logFile4PDR
	global coralLogFile
	
	if(nodeID == 1000): #all nodes
		nodeID=contiki_nodes #get the array of nodes

	if (getORset == 0) : # "get_parameters"
		param="get_parameters"
		return controller.execute_upi_function("radio","get_parameters",nodeID,upi)
	
	else: # "set_parameters"
		param="set_parameters"
		ret=controller.execute_upi_function("radio","set_parameters",nodeID,upi)
		#print("Executing set UPI: {}, responce: {}".format(upi, ret))
	
	line2write = "Executed UPI: "+str(upi) + ", on nodes: "+str(nodeID)
	
	#write in both log files
	write2logfile(logFile4PDR, line2write, str(datetime.datetime.now()) ) 
	write2logfile(coralLogFile, line2write, str(datetime.datetime.now()) )
	

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
	
	
	
# ===================== JSON RELATED ======================================
#try to send a JSON msg to JSS	
def sendJSON2JSS(json_msg):
	
	global conJSS, sockClient
	
	json_msg=str(json_msg)+str("\n") # be careful with "Can't convert 'dict' object to str implicitly"
	
	
	#print("Sending JSON: {}".format(json_msg)) #just debugging
	
	
	msg2JSS = bytes( json_msg,'UTF-8' )
	try:	
		sockClient.sendall( msg2JSS ) 
		#print ("JSON msg sent to JSS: " + json_msg ) #too much info
	except Exception as e:
		print("Error sending to JSS:"+str(e) )
		print("\nTrying to reconnect with javaSSConnection(1)\n")	
		#if the connection was reset close the connection and reconnect
		javaSSConnection(1) # asking for reset and reconnect


# python has problems with jsons with single quote ''
def setJSONcorrect(jIn):
	try:	
		jIn= json.dumps(jIn) #just json problems with '' & ""
		jIn=json.loads( jIn )
		return jIn
	except Exception as e:
		print ("JSON conversion problem: "+str(e) )		
# ================== JSON RELATED ====================================


					
#=================== UPI parsing =====================================
		

# use this to parse jsons coming from contiki UPIs.
# these jsons have the node as the first tag. so you have to know
# which station(s) was the UPI called against
def parseUPI_JSON (nodes, jsonIn, upiValue):
	if (nodes == 1000):	#all nodes
		nodes = contiki_nodes	
	for node in nodes: 
		n=str(node) # for json indexing: the first JSON taq is the station
		jsonIn = setJSONcorrect (jsonIn) # set JSON correctly					
		try:
			res = jsonIn[n][upiValue] 
			if (res):	
				line2write = " Node "+n+" "+upiValue+" "+str(res)					
				print ("Station "+n + upiValue+": " + str (res) )
				write2logfile (coralLogFile, line2write, str(datetime.datetime.now()))
		except Exception as e:
			pass # if the station is not in the json, continue


# jsonIn is the title of the UPI, e.g.: "CORAL_icmp_recv"
def parseUPI_JSON_aggr (nod, jsonIn, upiResult):
	
	global coralLogFile
	global contiki_nodes
	
	aggResult = 0 #return an aggragated result
	if (nod == 1000):	#all nodes
		nod = contiki_nodes	
		
	for node in nod: 
		n=str(node) # for json indexing: the first JSON taq is the station
		upiResult = setJSONcorrect (upiResult) # set JSON correctly					
		try:
			getRes = upiResult[n][jsonIn] 
			if (getRes):	
				line2write = "Node "+n+" "+jsonIn+" "+str(getRes)					
				#print (line2write+"\n" ) # uncomment this to check if all ok
				write2logfile (coralLogFile, line2write, str(datetime.datetime.now()))
			aggResult = aggResult + getRes
		except Exception as e:
			print ("json parsing problem: " +str(e) )
	print		
	line2write = str(jsonIn)+" for all nodes: "+str(aggResult) 
	write2logfile (coralLogFile, line2write, str(datetime.datetime.now()))
	print(line2write)

	return aggResult #a total number of packets
	
	
def analyzeInComeJSON(InComeJSON):  
	#Incoming set JSON example 
	#{"NID":2,"TYP":"set_parameter","CMD":{"IEEE802154_RPL_Doublings":8}}
	
	global  contiki_nodes	
	getORset =""
	upi=""				
	try: 
		InComeJSON=json.loads(InComeJSON.decode('utf-8') ) # if it is in JSON format
		
		InComeJSON =str(InComeJSON)
		InComeJSON = InComeJSON.replace("'", "\"")
		#print (InComeJSON)
		InComeJSON = json.loads(InComeJSON)
	except Exception as e: 
		print("JSON transformation problem: "+str(e) )	
	try:
		getORset = InComeJSON["TYP"]
		
		upi=InComeJSON["CMD"]
		

		node=InComeJSON["NID"] # specific node to sent the message to, or 1000 for all
		node= int(node)
		if node == 1000: #all nodes
			print("\nIncoming UPI: {} against ALL nodes".format(upi))
			#exec the UPI. DON'T SEND THE RESPONCE BACK! IT IS JUST ZEROS
			upi_exec(str(getORset),contiki_nodes,upi)
			
		else:
			print("\nIncoming UPI on node: {}: {}".format(node,upi))
			upi_exec(str(getORset),node,upi)
		
	except Exception as e: 
		print("JSON processing problem: "+str(e) )

	
		
# input just the UPI you want the result from ALL stations. RETURN a number
def gather_UPI_Stats_all(upi):
	global  contiki_nodes

	gather = controller.execute_upi_function("radio","get_parameters",contiki_nodes,[upi]) 

	sendJSON2JSS(gather)#send the json results to JSS. If not possible, try to reconnect
	return parseUPI_JSON_aggr(1000,upi,gather)
	
#========================== UPI parsing =====================================


#============ Sink Mote statistics ============================================
#calculate the pdr on sink and print the numbers 
def calcSinkPDR():
	
	global total_packets_recvd_sink

	#print("\nSINK mote (1) statistics:")	

	try:
	#total number of udp RECEIVED by sink
		nom =  controller.execute_upi_function("radio","get_parameters",1,["CORAL_udp_recv_total_sink"])
		nom = setJSONcorrect (nom)

		nominator =  nom["1"]["CORAL_udp_recv_total_sink"] 
		#print ("SINK says: Total UDP packets received: "+ str (nominator) )

		total_packets_recvd_sink = nominator # set the GLOBAL variable 
	except Exception as e:
		print ("CORAL_udp_recv_total_sink problem? "+ str(e) )
	 
	#total number of udp SENT by ALL stations. Aggregated by the sink
	denom = controller.execute_upi_function("radio","get_parameters",1,["CORAL_udp_send_total_sink"])
	
	#Send to CORAL JSS -->Node Red
	sendJSON2JSS(denom)

	denom= setJSONcorrect(denom)
	try:
		denominator =  denom["1"]["CORAL_udp_send_total_sink"] 
		
		line2write = "SINK says: Total UDP packets sent: "+str(denominator)
		#print(line2write)

		write2logfile ( coralLogFile, line2write, str(datetime.datetime.now()) )
	except Exception as e:
		print ("CORAL_udp_send_total_sink problem: "+str(e) )
 
	try: 
		#Packet Delivery Ratio (PDR) calculated in sink
		pdr = round( (nominator / denominator)*100 ,2) # percentage 

		line2write ="SINK says, PDR with sink statistics: "+str (pdr)+"%" 
		write2logfile (coralLogFile, line2write, str(datetime.datetime.now()) )

		#CLOSE THIS FOR TEMPORARY DEBUGGING
		#print(line2write)

	except Exception as e:
		print ("pdr calculation problem: "+str(e) )


#============ Sink Mote statistics =======================================


#================ Stations' Statistics ===================================
def calcStationsPDR (packetSendTotal):
	
	global total_packets_recvd_sink
	global logFile4PDR

	try:
		nominator = total_packets_recvd_sink #global variable
		if ( packetSendTotal>0 ):
			#Packet Delivery Ratio based on the statistics from stations
			pdrC = round( (nominator / packetSendTotal )*100 ,2) # percentage 
			line2write = "Stations' data PDR : "+str (pdrC)+"%" 
			print ("\n"+line2write)
			#write line to the main log file
			write2logfile (coralLogFile, line2write, str(datetime.datetime.now()) )
			justPDRline = "Stations_PDR: "+str(pdrC)+" %" # simple info
			#write to dedicated log file
			write2logfile( logFile4PDR, justPDRline, str(datetime.datetime.now()))
			#create JSON
			jsonUp = "{1: {'CORAL_pdr_total_sink':"+str(pdrC)+"}}"
			#print(jsonUp)
			#sends the results to CORAL JSS -->node-red 
			sendJSON2JSS(jsonUp)

		else:
			line2write ="packetSendTotal = 0 !" 
			print(line2write)
			write2logfile (coralLogFile, line2write, str(datetime.datetime.now()) )
	except Exception as e:
			print("stations' PDR calc problem: "+str(e) ) 		

#================ Stations' Statistics ===================================		

		
#================= RPL RELATED METHODS =======================================

# use this to change RPL Imin to node(s)	
def setrplImin(nodes, value):
		try:	
			print("changing RPL_Imin to nodes"+str(nodes) )			
			controller.execute_upi_function("radio","set_parameters",nodes,{"IEEE802154_RPL_Imin":value})
		except Exception as e:
			print("upi problem: "+str(e) ) 		
		print ("RPL changed succesful")


# use this to read ACTUAL RPL Imin value from node(s)	
def getrplImin(nod):

	for n in nod: 
		try:
			getRes=upi_exec(0, n,["IEEE802154_RPL_Imin"])
			jsonUp = getRes		
			#print("json 4 RPL Imin: {}".format(jsonUp)) #just debugging
			
			#sends the results to CORAL JSS -->node-red 
			sendJSON2JSS(jsonUp)

			if (getRes):	
				line2write = "Node "+str(n)+" RPL Imin: "+str(getRes)
				#if n == 2:				
					#print("printing Imin only for node 2:") #just debugging
				print (line2write ) # print ALL NODES
				write2logfile (coralLogFile, line2write, str(datetime.datetime.now()))
			print("\n")
		except Exception as e:
			print ("Imin json iteration problem: " +str(e) )
			
#================= RPL RELATED METHODS =======================================			
			

# ================= LOG FILES ================================================
def write2logfile (logfileName, line2write, time):
	#write values to a file inside dir ./logs 
	try:
		logfile = './logs/'+str(logfileName)
		#debugging 	
		#print ( "logfile to write the logs: {}".format(logfile))
		with open(logfile , "a") as myfile:
			 myfile.write( str(time) +", "+line2write+"\n" )
	except Exception as e:
		print("log file problem: "+str(e))


#create specific log file with ONLY stations' PDR
def createLogFile4PDR():
	global coralLogFile
	newName = coralLogFile[:-4] #remove the ".dat" part
	newName = str(newName)+"_nodes_PDR.dat"

	return newName		 
	

def createLogFile(): 
	global coralLogFile
	# the name of the file to keep the logs created here
	logFileName = str ( datetime.datetime.now() )
	coralLogFile = logFileName.replace(" ", "") +"_CORAL_log.dat"


def createLog5Min():
	global coralLogFile
	newName = coralLogFile[:-4] #remove the ".dat" part
	newName = str(newName)+"_5_min_stats.dat"
	return newName		 
		
#================ LOG FILES ============================================			
			



#========= Java Socks Client Related ==================================
def javaSSConnection(recon):
	global conJSS
	global sockClient
	
	# JSS IP or name and port. 4 now, it is in the SAME machine
	HOST = "localhost"
	PORT = 8999
	# Connect to the port on the server provided by the caller if you wish
	server_address=(HOST, PORT)
	
	if(recon ==1): 
		print("sockClient lost...")
		#reset the connection if it exists...
		try:
			print("Trying to close existing sockClient and reconnect...")
			sockClient.close()
			print("existing sockClient closed...")
			conJSS = False
		except Exception as e:
			print("sockClient closing error:"+str(e) )

	# Create a TCP/IP socket
	sockClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	while not conJSS:
		try:
			sockClient.connect(server_address)
			#connection is NON-Blocking. If else the program halts in sockClient.recv()
			#sockClient.setblocking(0) 
			print("\nConnected to CORAL JSS: " + HOST +":" + str(PORT) )
			conJSS=True
		except:# ??? Do we need to GC to wait 4 ever for the Java Server?
			print("No Java Server, waiting 5 secs...")
			time.sleep(5) # it will wait here 4 ever 4 Java Socks Server (JSS)  


def readlines(sockClient):
	#print("started readLines")	
	buff=1024
	delim=bytes('\n','utf-8')
	buffer = bytearray()
	strBuffer = ""
	data = True
	
	while data:
		#print("reading data inside readLines")
		data = sockClient.recv(buff)
		buffer += data

		while buffer.find(delim) != -1:
			line, buffer = buffer.split(delim, 1) 
			yield line
	return


def getSocksLines(sockClient,q):	
	for line in readlines(sockClient):
		q.put(line)  # Send line to main process


def runSocksProcess(sockClient,q):
	try:
		p = Process(target=getSocksLines, args=(sockClient,q))
		p.start()
		print (str(p) + " started")
	except Exception as e:
		print ("sockClient process exception: "+str(e) )

#========= Java Socks Client  Related ========================================


#==================== UDP Frequency Changing =================================
# use this to get RPL Imin value(s) from node(s)	
def getUDPFreq(nod):
	try:	
		upiResult = controller.execute_upi_function("radio","get_parameters",nod,["CORAL_send_interval"])
		print ("CORAL_send_interval upi result: "+str(upiResult))
		
		
		
		
		
		
		
		
		
		#this does not seem to work???????????????
		
		# running only against node 2
		#updFreq=upiResult[2]["CORAL_send_interval"] 
		
		#jsonUp = "{2: {'CORAL_send_interval':"+str(updFreq)+"}}" #prep this for node-red

		# check with antoni. is this ok??????????????
		#print("getUDPFreq JSON: {}".format(jsonUp)) #just debugging

		#sends the results to CORAL JSS -->node-red 
		#sendJSON2JSS(jsonUp)
		
	except Exception as e:
		print("UDP get UPI problem: "+str(e) ) 	
		return 0
	
	for node in nod: 
		n=str(node) # for json indexing: the first JSON taq is the station
		upiResult = setJSONcorrect (upiResult) # set JSON correctly					
		try:
			getRes = upiResult[n]["CORAL_send_interval"] 
			if (getRes):	
				line2write = "Node "+n+" UDP Send Freq: "+str(getRes)					
				print ("\n"+line2write+"\n" )
				write2logfile (coralLogFile, line2write, str(datetime.datetime.now()))
		except Exception as e:
			print ("UDP Send Freq json parsing problem: " +str(e) )
		
#==================== UDP Frequency Changing =================================


#=================== LATENCY FOR ALL STATIONS ================================
def latency_extract (contiki_nodes,jsonIn):

	TICKS_PER_SECOND = 32000 #can be taken from contiki with UPI in the future ???
	millisecs = TICKS_PER_SECOND / 1000
	
	global latency_diff
	global packets_received
	global current_jitter
	global oldLatency

	jitterAvg = 0 # find the average jitter for EACH round
	
	
	#jsonIn = setJSONcorrect (jsonIn) # set JSON correctly					
	try:
		res =jsonIn[1]["CORAL_latency"] 
		#print(res)
	except Exception as e:
		print("jitter return problem: "+str(e))
		
	print("\n------------------------- latency --------------")
	try: 
		for position, node in enumerate(contiki_nodes):
			if not (node == 1): #node 1 has no latency
				#print("node: {}, in pos: {}".format(node,position) )	#Debuggining
				try: 
					#print("node {} incoming latency {}".format(node,res[node]))
					
					
					
					
					
					
					# ARE YOU SURE ABOUT THIS ???????????????????????????????????????????????
					latency_ms =   res[node] /  millisecs #convert to milliseconds
					
					
					
					
					
					
					
					latency_float = round(latency_ms,5) #only five digits
					line2write = "Node "+str(node)+" CORAL_latency (ms): "+str(latency_float)
					write2logfile (coralLogFile, line2write, str(datetime.datetime.now()))		
					
					#dont print the latency of every node
					#print(line2write)
					

					jsonUp  = "{"+str(node)+":{'CORAL_latency'"+": "+str(latency_float)+"}}"
					sendJSON2JSS(jsonUp) #send to JSS -->Node Red
				
				except Exception as e:
					print("latency assignment problem: "+str(e))
				
				
				try:
					oldVal = oldLatency[position]
					#print("oldVal: {} in latency_diff[{}]".format(oldVal,position))#Debugging
				except IndexError as e: # the 1st time the list is empty...
					oldLatency.append(latency_float)
					print("oldLatency problem: "+str(e))
					pass
			
				
				try:
					cur_latency_diff = (abs) ( oldVal - latency_float) #absolute value
					cur_latency_diff = round(cur_latency_diff,5) #only five digits
					
					latency_diff.insert(position,cur_latency_diff)
					oldLatency.insert(position,latency_float) # last value in global var
					print("Node {}: latency difference: {}".format(node,cur_latency_diff))			
				except IndexError as e: # the 1st time the list is empty...
					latency_diff.append(latency_float)
					print("latency_diff problem: "+str(e))
					pass

				try:
					packs = packets_received[position]
					#print("packets_received[{}]: {}".format(position,packs))
					packets_received.insert(position, packs+1)
					

					
					#print("packet counting for node {}:{}".format(node, packs))
					

					
				except IndexError as e: # the 1st time the list is empty...
					print("Node "+str(node)+": packet index: "+str(e))
					packets_received.append(1)#the list is in the correct position
					#print("packets_received["+str(position)++"]: "+packets_received[position])
					pass
			
				try:
					jitter = latency_diff[position] / packets_received[position]
					jitter = round(jitter,5) #only five digits
					
					#print("position {}, jitter: {}".format(position,jitter)) #use for verification
					current_jitter.insert (position, jitter )
					line2write = "Node {} jitter: {}".format(node,jitter)

					#dont print the jitter of every node
					#print(line2write)
					
					write2logfile (coralLogFile, line2write, str(datetime.datetime.now()))	
					jsonUp  = "{"+str(node)+":{'jitter'"+": {}}}".format(jitter)
					sendJSON2JSS(jsonUp) #send to JSS -->Node Red

					jitterAvg = jitterAvg + jitter #adding all nodes's jitters
					#print("jitterAvg: {}".format(jitterAvg))

				except IndexError as e: # the 1st time the list is empty...
					current_jitter.append(latency_diff)
					print("current_jitter index: "+str(e))
					
			print ("") #just between nodes			
		
		try: # AVERAGE JITTER of all nodes: THIS IS A CORRECT MEASUREMENT (DIFF ONLY)
		
			jitterAvg = jitterAvg / (len(contiki_nodes)-1) # remember No 1 has no jitter
			jitterAvg = round(jitterAvg,5) #only five digits
			
			print ("AVERAGE jitter: {}".format(jitterAvg) )
			
			line2write = "AVG jitter: {}".format(jitter)
			write2logfile (coralLogFile, line2write, str(datetime.datetime.now()))	
			jsonUp  = "{"+"1000"+":{'jitter'"+": {}}}".format(jitter)
			sendJSON2JSS(jsonUp)
		except Exception as e:
			print ("jitter not ready yet: "+str(e))
			
	
	except Exception as e:
		print ("for loop in latency problem: "+str(e))
				
	print("------------------------- latency --------------\n")

#=================== LATENCY FOR ALL STATIONS ================================




#=== it will wait here 4 ever until Java Socks Server (JSS) is found ============			
def main(args):
	createLogFile() #create a new log file
	
	global total_packets_recvd_sink
	global contiki_nodes  #be careful with this.. If not global, it will not be GLOBALLY shared
	global sockClient

	printWaitNodesMsg=True # Just to control the on screen messages...

	javaSSConnection(0) # (0) is first time to connect. Reconnection is (1)
	q = Queue()
	runSocksProcess(sockClient,q)

	global logFile4PDR
	logFile4PDR = createLogFile4PDR() # create once the global var
	
	global coralLogFile
	# counting 5min segments
	global FiveMinlogName 
	FiveMinlogName = createLog5Min()#separate log file
	min_5_counter = time.time()
	icmpS_5min_Start = 0
	icmpR_5min_Start = 0
	udpS_5min_Start = 0
	total_packets_5min_Start = 0
	
	#just to execute experiments. E.g. every 1/2 change the packet sending timer
	fifteen_min_counter = time.time()
	Imin_min_set = False #setting Imin = 8 and if true  Imin = 13
	udpPacketsFreq_min = True
	
	
	
	#control loop; RUNNING FOR EVER........
	while True:
	
	
		contiki_nodes = controller.get_mac_address_list()
		if contiki_nodes: # If there is at least one node
			#print("\nConnected nodes:", [node for node in contiki_nodes]) #too much info....
			
			# Using Queues to send the request up to the contiki_nodes			
			if not q.empty():
				command = q.get()  # Get line from reading process
				analyzeInComeJSON(command)

			#prints tot_packets send(aggregated in sink, received and pdr
			#it is different in sink vs motes: when mote is lost, sink is dumb		
			calcSinkPDR() # it will also send the tot_pack_recevd to CORAL JSS -->Node-red

			print("\nPrinting Station(s) stats:" )
			
			# total control packets sent from all stations
			icmpS =  gather_UPI_Stats_all("CORAL_icmp_send") 
			jsonUp = "{1:{'CORAL_icmp_send_total_sink':"+str(icmpS)+"}}"
			
			# I AM AFRAID I AM SENDING IT TwICE !!!!!!!!!!!!!
			sendJSON2JSS(jsonUp) #send to JSS -->node-red			
			
			# control msgs received by all stations
			icmpR = gather_UPI_Stats_all("CORAL_icmp_recv") 
			
			# total data packets send from all stations
			udpS = gather_UPI_Stats_all("CORAL_udp_send") 
			
			#calculate the PDR based on stations' stats, FROM THE BEGGINING OF TIME
			calcStationsPDR(udpS)
	
	
	
	
	
	# DISABLED. USED FOR TESTING....

# ========== Changing send interval every fifteen minutes ==============================
			fifteen_min_check = time.time() - fifteen_min_counter
			#print ("\nfifteen_min_check current value: {} secs".format( round(fifteen_min_check,0) ))
			
			#if ( fifteen_min_check > 900): #900 ): # fifteen min = 15mins*60 = 900
			
			if(1 == 2): #always false. 
			
				print("\nfifteen minutes timer reset...")
				fifteen_min_counter =  time.time() # reset 
				if (udpPacketsFreq_min):
					udpPacketsFreq_min = False	
					line2write = "UPI: set_parameters"+str(contiki_nodes)+"{CORAL_send_interval:5}"
					print("Executing: {}".format(line2write))
					upi_exec("set_parameters",contiki_nodes,{'CORAL_send_interval':5})					
					# log the UPI changes to 5 mins log file	
					write2logfile (FiveMinlogName, line2write, str(datetime.datetime.now()))
					# log to PDR logging file also
					write2logfile (logFile4PDR, line2write, str(datetime.datetime.now()) )
				else:
					udpPacketsFreq_min = True	
					line2write = "UPI: set_parameters"+str(contiki_nodes)+"{CORAL_send_interval:1}"
					print("Executing: {}".format(line2write))
					upi_exec("set_parameters",contiki_nodes,{'CORAL_send_interval':1})				
					# log the UPI changes to 5 mins log file	
					write2logfile (FiveMinlogName, line2write, str(datetime.datetime.now()))
					# log to PDR logging file also
					write2logfile (logFile4PDR, line2write, str(datetime.datetime.now()) )
# ========== Changing send interval every fifteen minutes ===========================				
					
					
					
					
					
					
					
					
					
					
					
					
					
					
					
					
					
					
					
					
					
					
					
			
#=============== Five (5) minutes counters ==========================================		

			time_dif = time.time() - min_5_counter
			five_min = datetime.timedelta(seconds = int(time_dif)) # just demo of timedelta. Not used
			if ( time_dif < 300 ): #300secs=5min
				#get the current values
				icmpR_5min_End = icmpR
				udpS_5min_End = udpS
				icmpS_5min_End = icmpS
				
				total_packets_5min_End = total_packets_recvd_sink #get global var

				#print("Within last 5 min, counting packets: icmpR:{}, udpS:{},icmpS:{}".format(icmpR_5min_End,udpS_5min_End,icmpS_5min_End)) 
				print ('\nCounting 5 min: {} \n'.format( datetime.timedelta(seconds = int(time_dif))) )
				
				#minutes = divmod(time_dif, 60)
				#print ('\nElapsed time: {} mins, {} secs\n'.format(round(minutes[0],0),round(minutes[1],1)) )
				
			else:
				print("\n------- After the last five (5) mins -------------")
				
				try:
					icmpR_5min = icmpR_5min_End -icmpR_5min_Start
					icmpS_5min = icmpS_5min_End -icmpS_5min_Start
					udpS_5min = udpS_5min_End -udpS_5min_Start
					
					#print ("icmpR_5min_End:"+str(icmpR_5min_End))
					line2write ="icmp packets received: {}".format(icmpR_5min)
					print(line2write)
					write2logfile (FiveMinlogName, line2write, str(datetime.datetime.now()))	
					
					line2write ="icmp packets send: {}".format( icmpS_5min )
					print(line2write)
					write2logfile (FiveMinlogName, line2write, str(datetime.datetime.now()))	
					
					line2write ="udp packets send: {}".format( udpS_5min )
					print(line2write)
					write2logfile (FiveMinlogName, line2write, str(datetime.datetime.now()))	
					
					#ratio between control & data packets
					line2write ="icmp 2 udp ratio: {}".format( round ( (udpS_5min / icmpS_5min ) ,2) )
					print(line2write)
					write2logfile (FiveMinlogName, line2write, str(datetime.datetime.now()))	
					
					
					#ratio between send vs received data packets
					line2write ="received 2 send packets ratio: {}".format( round(total_packets_5min_Start / total_packets_5min_End ,2) )
					print(line2write)
					write2logfile (FiveMinlogName, line2write, str(datetime.datetime.now()))
					write2logfile (FiveMinlogName, "--------------", str(datetime.datetime.now()))
					
					#reset all the 5min counters
					print("\n...FIVE MIN COUNTERS RESET...\n")
					min_5_counter = time.time()
					icmpR_5min_Start = icmpR_5min_End
					icmpS_5min_Start = icmpS_5min_End
					udpS_5min_Start = udpS_5min_End
					total_packets_5min_Start = total_packets_5min_End
					
					#print("Starting with icmpR: {}, icmpS: {}, udpS: {}, total_packets: {}".format(icmpR_5min_Start,icmpS_5min_Start,udpS_5min_Start,total_packets_5min_Start))
				
				except Exception as e:
					print("five min stats:"+str(e))
					
				print("------- End of five (5) mins stats ------------------\n")
#=============== Five (5) minutes counters ===========================================




#======= ATTENTION: SENDING THE FIVE MINUTES INTERVAL ===============================		
				#CORAL_udp_vs_control
				try:
					packet_ratio = (float) (udpS_5min / icmpS_5min)
					print("Five mins packet ratio: (udp / icmp) : {}\n".format(round(packet_ratio,3)))
					jsonUp = "{1:{'CORAL_udp_vs_control':"+str(packet_ratio)+"}}"
					sendJSON2JSS(jsonUp) #send to JSS -->node-red
				except Exception as e:
					pass
#======= ATTENTION: SENDING THE FIVE MINUTES INTERVAL ============================			
			



#======= SENDING THE HISTORICAL DATA (FROM BEGGINING OF TIME. SLOW CHANGES) =====

			#CORAL_udp_vs_control
			#packet_ratio = (float) (udpS / icmpS)
			#print("packet ratio: (udp / icmp) : {}".format(round(packet_ratio,3)))
			#jsonUp = "{1:{'CORAL_udp_vs_control':"+str(packet_ratio)+"}}"
			#sendJSON2JSS(jsonUp) #send to JSS -->node-red			
			
			#jsonUp = "{1:{'CORAL_udp_send_total_sink':"+str(udpS)+"}}"		
			# make sure you dont send IT TwICE !!!!!!!!!!!!!
			#sendJSON2JSS(jsonUp) #send to JSS -->node-red
#======= SENDING THE HISTORICAL DATA (FROM BEGGINING OF TIME. SLOW CHANGES) =====			
			


			
			print("------------ General Stats -----------------")
			#RPL Imin Periodically Reading all nodes & send to JSS -->node-red
			getrplImin(contiki_nodes)			
			
			
			
			
			
			
			
			#Periodically read UDP sending frequency (From 1:1 to 1:10, 10=times more)
			#for the moment, ALL have the same. So ask only No 2 (Sink does NOT send UDP)
			
			#getUDPFreq([2])
			# ?????????????????
			
			
			
			
			
			
			
			
			#for node in contiki_nodes:
			#	latency[node]=controller.execute_upi_function("radio","get_parameters",[1],["CORAL_latency"]
			
			
			
			
			#wtf is that ???????????????????????????????????????????????????????????????
			latency = controller.execute_upi_function("radio","get_parameters",contiki_nodes,["CORAL_latency"]) 
			latency_extract (contiki_nodes,latency)


				
			



#============ METHODS ========================================================
			# use these methods:
			#def setrplImin(nodes, value):
			# def setJSONcorrect(jIn)
			#def calcSinkPDR()
			#def write2logfile (logfileName, data, time) # time as string
			#def parseUPI_JSON (nodes, jsonIn, upiValue)
			#def parseUPI_JSON_aggr (nodes, jsonIn, upiValue)
			#write2logfile		
			#def setrplImin(nodes, value):

#============= UPIs ==========================================================
		#"CORAL_icmp_send",6651,"UINT16_T",2,"PARAMETER","","",">"
		#"CORAL_icmp_recv",6652,"UINT16_T",2,"PARAMETER","","",">"
		#"CORAL_udp_send",6671,"UINT16_T",2,"PARAMETER","","",">"
		#"CORAL_udp_rcv_total",6672,"UINT16_T",2,"PARAMETER","","",">"
		#"CORAL_send_interval",6685, "UINT16_T",2,"PARAMETER","","",">"
		
		#"IEEE802154_phyCurrentChannel",51638,"UINT8_T",1,"PARAMETER","","",">"
		#"IEEE802154_phyTXPower",58914,"UINT8_T",1,"PARAMETER","","",">"
		#"IEEE802154_macShortAddress",55909,"UINT16_T",2,"PARAMETER","","",">"
		
		#PERIODIC example of calling a UPI. Returns a JSON
		#def upi_exec(getORset, contiki_node, upi)
		#ret=upi_exec(0, 0,["IEEE802154_RPL_Imin"])
		#print("responce :"+str(ret[0]) )  #the 2nd part of the message is a json
		#sendJSON2JSS(ret)
			
		#Example of set UPI
		#ret = controller.execute_upi_function("radio","set_parameters",contiki_nodes,{'IEEE802154_phyCurrentChannel':12})
		#print("....{}".format(ret))		
#============= UPIs ==========================================================



#************************* END OF if(nodes) **********************************
		else: #if nodes
			if printWaitNodesMsg:
				print ("\nNo node yet. Probing every 5 secs...")
				printWaitNodesMsg= False # it will print the above message only once...
		
		
		

		
		# If the controller is heavilly loaded, this is not needed....			
		#gevent.sleep(15)
			
			

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
