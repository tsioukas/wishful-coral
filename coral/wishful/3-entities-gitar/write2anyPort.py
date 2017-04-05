#!/usr/bin/python

import serial
import time
from multiprocessing import Process, Pipe
import getPTSports #find the avaliable serial port on the local machine 
from random import randint #just for random tests...
import threading

#initialization and open the port

#possible timeout values:
#    1. None: wait forever, block call
#    2. 0: non-blocking mode, return immediately
#    3. x, x is bigger than 0, float allowed, timeout block call

ser = serial.Serial()
ser.port     # set later accordingly
ser.baudrate # set later accordingly

ser.bytesize = serial.EIGHTBITS #number of bits per bytes
ser.parity = serial.PARITY_NONE #set parity check: no parity
ser.stopbits = serial.STOPBITS_ONE #number of stop bits
#ser.timeout = None          #block read
ser.timeout = 1            #non-block read
#ser.timeout = 2              #timeout block read
ser.xonxoff = False     #disable software flow control
ser.rtscts = False     #disable hardware (RTS/CTS) flow control
ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
ser.writeTimeout = 2     #timeout for write


def setupPort(serPort, serBaudRate): 
	ser.port = serPort 
	ser.baudrate = serBaudRate
	if not ser.isOpen():
		try: 
			ser.open()
			#print ("port is:"+str(serPort)+" bRate="+str(serBaudRate) )
		except Exception as e:
			print ("Write port error: " +str(e) )
			print ("\nExit :-(")
			exit()


def writePort(data2write):
	if ser.isOpen():
		try:
			data2write = (data2write+"\n").encode()  #BE CAREFUL: IT NEEDS \n !!!!!!
			#print("Write serial: bytes msg to sent to UART: "+str(data2write) )
			ser.flushInput() #flush input buffer, discarding all its contents
			ser.flushOutput()#flush output buffer, aborting current output 

			#write data and discard all that is in buffer
			ser.write(data2write)

			time.sleep(0.5)  #give the serial port sometime to receive the data
			print("Write to UART ok...\n")	
		except Exception as e:
			print ( "Write serial error: " + str(e) )
	else:
		print ( "Write serial error: Could not open port. Msg not sent..." )


#-----------use this for writing to the port-----------------#
def writeThis(portName, brate, data2write):
	try:
		setupPort(portName,brate)#if the port does not open, the program will exit
		writePort (data2write )
	except Exception as e:
		print("Write serial error: "+str(e) )
#-----------use this for writing to the port-----------------#


# ONLY for Testing: Writing continiously a msg to the serial port
def writeCont(portName, brate):

	while True:
		rnd=randint(0,9)
		
		data2write="hello"+str (rnd)
		print ("msg: " + data2write + " --> " + portName )
		writeThis(portName, brate, data2write)
			
		print ("sleeping for : " + str(rnd) + "in port " + portName )
		time.sleep(rnd)

#if __name__ == '__main__':

