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
		#ser.close();

		try: 
			ser.open()
			print ("port is:"+str(serPort)+" bRate="+str(serBaudRate) )
		except Exception, e:
			print str(e)
			print "exiting :-("
			exit()


def writePort(data2write):
	if ser.isOpen():
		try:
			ser.flushInput() #flush input buffer, discarding all its contents
			ser.flushOutput()#flush output buffer, aborting current output 
			print ("msg is = " + data2write )
			#write data
			#and discard all that is in buffer
			ser.write(data2write)

			time.sleep(0.5)  #give the serial port sometime to receive the data

			#ser.close()
		except Exception, e1:
			return "error: " + str(e1)
	else:
		return "cannot open serial port" 



#-----------use this for writing to the port-----------------#
def writeThis(portName, brate, data2write):

	#prepare data for sending. Needs carriage return: "\n"
	data2write=str(data2write)+"\n"
	try:
		setupPort(portName,brate)#if the port does not open, the program will exit
		writePort (data2write)
		#writeProcess = Process(target=writePort, args=[data2write])
		#writeProcess.start()
	except:
		pass
#-----------use this for writing to the port-----------------#


# ONLY for Testing: Writing continiously to the serial port
def writeCont(portName, brate):

	while True:
		rnd=randint(0,9)
		
		data2write="hello"+str (rnd)
		print ("msg: " + data2write + " --> " + portName )
		writeThis(portName, brate, data2write)
			
		print ("sleeping for : " + str(rnd) + "in port " + portName )
		time.sleep(rnd)

#if __name__ == '__main__':

