#!/usr/bin/env python

# 11.10.2016

import socket
import sys
import json
import threading
import time

# Server IP or name and port
HOST = "localhost"
PORT = 8999

server_address=(HOST, PORT)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#print >>sys.stderr, 'connecting to ' + HOST +':' + str(PORT)
# Connect the socket to the port on the server given by the caller

# create a (static) json object
data={}



class Client():
	
	# Server IP or name and port
	HOST = "localhost"
	PORT = 8999

	server_address=(HOST, PORT)


	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	con=False
	while not con:
		try:
			sock.connect(server_address)
			con=True
		except:
			print("no Java server connection possible")
		finally:
			time.sleep(5)
		
	print("connected to Java....")
	
	# call this to continioulsy receive from server
	def start(self):
		#while True:
			amount_received = 0
			amount_expected = 500 #maximum message length
			
			length ="" # the length of the incoming message
			data=""	# the rest of the JSON message
			while amount_received < amount_expected:
				amount_received += len(data)
				current = sock.recv(1) # one char at the time
				length+= current.decode("utf-8")
				if (current == "{"):
					length= length [:-1] 
					amount_expected = int(length)
					print ("amount_expected="+str(amount_expected) )
				else:
					data+=current.decode("utf-8")
					#print ("datalength:"+str(len(data)) )
				#print >>sys.stderr, 'received "%s"' % data
			#print ("msg="+data)
			return data
			
	    
	def sendS(self,data):
		sock.send("ddd".encode() )
		#sock.send(bytes(data, 'UTF-8') )
		#sock.send(format(data) )
		
	# call this to send a message to the server connected to	
	def sendMsg(self,data):	
		#msg=json_add("key1","data1")
		#print >>sys.stderr, 'sending "%s"' % msg
		#sock.sendall(data.encode() )
		sock.send(2)
		#sock.sendall(format(data) )
		
	def json_add(key, value):
		data[key]=value
		json_data=json.dumps(data)
		return json_data
		
	def printTest(self):
		print("I am alive!")
    
#finally:
#    sock.close()

#t1=threading.Thread(target = Client() )
#cl=Client()
#t2 = threading.Thread (target= cl.start() )
#t3 = threading.Thread (target= cl.sendS("rr"))
#cl.start()
#print ("receiving finished")
#cl.sendMsg()
#json = json_add("keyyyy", "vasffsgadsfl")
#print ("Sending to server:"+json)
#cl.sendS(json+"\n")




