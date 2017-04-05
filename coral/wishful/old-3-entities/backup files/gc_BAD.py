#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
wishful_controller_simple.py: First implementation of WiSHFUL controller

Usage:
   wishful_controller_simple.py [options] [-q | -v]

Options:
   --logfile name      Name of the logfile
   --config configFile Config file path

Example:
   ./wishful_simple_local_controller -v --config ./config.yaml 

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
import wishful_controller
import gevent
import yaml
import wishful_upis as upis
import json
import time
import socket

from lc import write2Serial, readFromSerial
from threading import Thread
import threading
import printThread


__author__ = "Piotr Gawlowicz, Mikolaj Chwalisz"
__copyright__ = "Copyright (c) 2015, Technische Universität Berlin"
__version__ = "0.1.0"
__email__ = "{gawlowicz, chwalisz}@tkn.tu-berlin.de"


#========= Java Socks Client ======================================

# Server IP or name and port
HOST = "localhost"
PORT = 8999
# Connect to the port on the server given by the caller if you wish
server_address=(HOST, PORT)
# Create a TCP/IP socket
sockClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("\nTrying to connect to " + HOST +":" + str(PORT) )

con=False #starting with no connection
while not con:
	try:
		sockClient.connect(server_address)
		print("Connected to above Java Socket Server (JSS)...") 
		print
		con=True
	except:# Do we need to GC to wait 4 ever for the Java Server?
		print("\nNo Java Server, waiting 5 secs...\n")
		time.sleep(5)
#======= it will wait here until Socks Server is found ============


log = logging.getLogger('wishful_agent.main')
controller = wishful_controller.Controller()
nodes = []


@controller.new_node_callback()
def new_node(node):
	global sockClient
	nodes.append(node)
	print("GC: New node appeared:"+node.name)
	#print(node) # prints tons of info
	#print("Calling \"readFromNode()\" for the node above...\n")
	#readFromNode(node)

	msgTag="CtrlMsg"
	
	#be careful: it crashes if no node was found YET....
	#startRfromJS(msgTag)
	
	startRead4Ever(node)

@controller.node_exit_callback()
def node_exit(node, reason):
    if node in nodes:
        nodes.remove(node);
    print("NodeExit : NodeID : {} Reason : {}".format(node.id, reason))


@controller.set_default_callback()
def default_callback(group, node, cmd, data):
    print("GC: DEFAULT CALLBACK : Group: {}, NodeName: {}, Cmd: {}, Returns: {}".format(group, node.name, cmd, data))


# need to SERIOUSLY RESEARCH ON THIS
@controller.add_callback(upis.net.get_info_of_connected_devices)
def get_info_of_connected_devices_reponse(group, node, data):
    global log
    log.info("get_info_of_connected_devices_reponse : Group:{}, NodeName:{}, msg:{}".format(group, node.name, data))
    print ("get_info_of_connected_devices_reponse : Group:{}, NodeName:{}, msg:{}".format(group, node.name, data))
    
    
def write2node (node,msgTag, msgBody):
	#print("GC: Node:" + str(node.name) )
	msg={msgTag:msgBody}
	lc_name="lc_"+str(node.name)	
	lc = controller.node(node).hc.start_local_control_program(program=write2Serial )  
	lc.send(msgBody) # send only msgBody  to the LC

			
#def startRead4Ever(lc):
def startRead4Ever(node):
	global sockClient
	
	lc = controller.node(node).hc.start_local_control_program(program=readFromSerial)
	
	while True:
		msg = lc.recv(timeout=2)
		if msg:
			print ("GC: Msg from LC_id:"+str(lc.id) )#+":{}".format(msg) )
			
			#msgG=[{"CtrlMsg"}] #???????????????????
			#msg={msgG}
			msgString = str(msg)
			print ("Msg is: "+ msgString)
			
			#send the received msgG to Java
			sockClient.sendall(bytes(msgString+"\n",'UTF-8') ) 
			print ("msg sent to Socks Server: " + msgString)


def readFromNode (node):
	lc = controller.node(node).hc.start_local_control_program(program=readFromSerial)
	t1 = threading.Thread( target = startRead4Ever, args=(lc,) )
	t1.start()
	print ("Reading from LC.id:"+str(lc.id)+ ", thread="+t1.name )
	
	
def getMsgFromJS(msgTag):
	global nodes

	while True:
		print("\n....Waiting for JSS to send something....\n")
		current = sockClient.recv(1024) #waiting for the Socks Server to send something
		if current:
			# insert switch statements here...........
			try:
				node=nodes[0] #node number. get it from JSS
				socksMsg = current.decode('UTF-8')#get a msg from Socks Server
				if (node in nodes):
					strSocksMsg=str(socksMsg)
					print ("JSS msg: "+ strSocksMsg )
					print ( "GC: Sending msg to node:" +node.name)
					
					#lc = controller.node(node).hc.start_local_control_program(program=write2Serial )
					#lc.send(strSocksMsg)
				else:
					print("Such node does not exist! Msg discarded")
					log.debug("Such node does not exist!")
			except:
				print("Node not found. I will do NOTHING!")


def startRfromJS(socksMsg):
	t1 = threading.Thread( target = getMsgFromJS, args=(socksMsg,) )
	t1.start()
	print("Write thread started:"+t1.name+"\n" )

	
def main(args):
	log.debug(args)

	config_file_path = args['--config']
	config = None
	with open(config_file_path, 'r') as f:
		config = yaml.load(f)

	controller.load_config(config)
	controller.start()

	#testing
	sockClient.sendall(bytes ("Just testing. Ignore"+"\n", 'UTF-8') )
	print("Sent a test msg to JSS")

	msgTag="CtrlMsg"
	#print("Starting the \"getMsgFromJS()\"" )
	#getMsgFromJS(msgTag) #fail safe. If node is not found, it does nothing

	#control loop
	while True:
		if nodes:
			print ("\nNode(s) found. Sleeping 5 secs...\n")
			#for n in nodes:
			
				#print ("Node appeared:"+n.name)
				#wait to read something
				#readFromNode(n,sockClient)

				#send a message to node
				#write2node (n,msgTag, "TD")
				
				#startRfromJS(n,msgTag)
			gevent.sleep(5)
		#else:
		#gevent.sleep(5)

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

try:
	main(args)
except KeyboardInterrupt:
	log.debug("Controller exits")
finally:
	log.debug("Exit")
	controller.stop()
