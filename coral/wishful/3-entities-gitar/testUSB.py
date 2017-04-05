#!/usr/bin/python

from sockClientThread import sockClient
import threading
#import serial
#from write2anyPort import writeThis

#writeThis('/dev/ttyUSB0', 115200,"TD")

#thread1 = sockClient("sock").start()

import socket

def socks():

	# JSS IP or name and port. 4 now, it is in the SAME machine
	HOST = "localhost"
	PORT = 8999
	# Connect to the port on the server provided by the caller if you wish
	server_address=(HOST, PORT)
	
	
	started = False
	probleMsg = False
	while not started:
		try:
			sockClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sockClient.connect(server_address)
			started = True
			print ("Starting sockClient...")
			result = sockClient.recv(1024)
			print("result = "+str(result) )
		except Exception as e:
			if not probleMsg:
				print("socks problem: "+str(e) )
				print("will keep on trying 4 ever...")
				probleMsg = True			
				
def trythese():
	while True:
		try: 
			t1 = threading.Thread(target=socks, args=())
			t1.start()
			t1.join()
		except Exception as e:
			print ("thread exception: "+str(e) )

trythese()

#while not sockClient("sock").start().isAlive():
#thread1 = sockClient("sock").start()
