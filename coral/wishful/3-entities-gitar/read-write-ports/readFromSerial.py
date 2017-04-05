#!/usr/bin/python

# be careful: import serial does not work with python3
# it obviously needs pip installation of pyserial.
#be careful: Only install for v3 in (dev)user@....
import serial

   
import time
from multiprocessing import Process, Pipe
import getPTSports #find the avaliable PSEUDO serial port on the local machine 
from random import randint #just for random tests...
from threading import Thread
import json

#initialization and open the port

#possible timeout values:
#    1. None: wait forever, block call
#    2. 0: non-blocking mode, return immediately
#    3. x, x is bigger than 0, float allowed, timeout block call


def readPort(serPort, serBaudRate):

	ser = serial.Serial()
	#ser.port     # set later accordingly
	#ser.baudrate # set later accordingly

	ser.bytesize = serial.EIGHTBITS #number of bits per bytes
	ser.parity = serial.PARITY_NONE #set parity check: no parity
	ser.stopbits = serial.STOPBITS_ONE #number of stop bits
	ser.timeout = None          #block read
	#ser.timeout = 1            #non-block read
	#ser.timeout = 2              #timeout block read
	ser.xonxoff = False     #disable software flow control
	ser.rtscts = False     #disable hardware (RTS/CTS) flow control
	ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control

	ser.port = serPort 
	ser.baudrate = serBaudRate
	
	if not ser.isOpen():
		try: 
			ser.open()
		except Exception as e:
			print ("Read serial error:"+str(e)+"\nExiting now") #error opening serial port
			exit()

	if ser.isOpen():
		try:
			ser.flushInput() #flush input buffer, discarding all its contents
			ser.flushOutput()#flush output buffer, aborting current output 
			#and discard all that is in buffer
			while True:
				print( "Read serial: Waiting...") 
				response = ser.readline()
				if response:# it only reacts if response != null
					#return response
					#printThis(ser.port,response)#!!!!!!!!!!!
					print("Received from UART: " + str(response) )
					#j={} # JSON create
					#j["\""+str(controller.id)+"\""]=str(response)
					#json_data=json.dumps(j)
					#controller.send_upstream(json_data)  
					#returnThis(response)#!!!!!!!!!!!!!!			       
			ser.close()
		except Exception as e1:
			print ( " Read serial error: "+str(e1) )
		else:
			print ( "Read serial error (port not open?)" ) 
	else:
		print ("Read serial: port is closed")

# Calling this from the read function
def printThis(port, data):  
	print ("port: " + port + ", received: "+data)  

#just return the data whenever received...
def returnThis(data):
	#sendThread=Thread(target=returnThis(data) )
	print ("data received ok")
	return data	

#------------- call this from outside -----------------"
def StartRead(serPort, serBaudRate):
	answer = readPort(serPort, serBaudRate)
	return answer
#------------- call this from outside -----------------"



#------------- call this from outside -----------------"
def StartReadThread(serPort, serBaudRate, controller):
	readProcess = Thread(target=readPort, args=(serPort, serBaudRate, controller,) )
	#if readProcess.isAlive()==False:
	readProcess.start()

	
#------------ call this from outside -----------------"


#if __name__ == '__main__':

#	StartRead("/dev/pts/21", 115200)
