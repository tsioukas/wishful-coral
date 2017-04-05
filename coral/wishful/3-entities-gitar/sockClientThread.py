#!/usr/bin/python

import threading
import time
import socket

noThread = True

# JSS IP or name and port. 4 now, it is in the SAME machine
HOST = "localhost"
PORT = 8999
# Connect to the port on the server provided by the caller if you wish
server_address=(HOST, PORT)
	
class sockClient (threading.Thread):
	
	def __init__(self, sock):
		threading.Thread.__init__(self)
		started = False
		probleMsg = False
		while not started:
			try:
				self.sockClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.sockClient.connect(server_address)
				self.result = ""
				started = True
			except Exception as e:
				if not probleMsg:
					print("socks problem: "+str(e) )
					print("will keep on trying 4 ever...")
					probleMsg = True
		
	def run(self):
		try:
			print ("Starting sockClient...")
			result = self.sockClient.recv(1024)
			#self.sockClient.close()
			#printRes( )
			return result
		except Exception as e:	
			self.sockClient.close()
			print("socks server gone: "+str(e) )
			thread1 = sockClient("sock")
			thread1.start()
			
			
def printRes():
		print (self.result)
		print("thread exits, creating new thread")
		
		thread1 = sockClient("sock")
		thread1.start()
		return result



thread1 = sockClient("sock").start()
#thread1.start()
print ("sockClient Threads started...")
