#!/usr/bin/python

import findAllSerialPorts
import write2USB0
import write2anyPort
from threading import Thread
import readFromSerial
import getPTSports

if __name__ == '__main__':

	ptsports=getPTSports.getAllpts()
	print ("ptsports portsfound:")
	print ptsports
	print 
	
	for i in range(len(ptsports)-1): #there is an empty record at the end !!!!
		d="d"+str(i)
		#d = Thread(target=readFromSerial.readPort, args=(ptsports[i],115200,))
		msg=readFromSerial.readPort(ptsports[i],115200,)
	#while True:
		#res=d.start()
		print msg
		

	#for pts in ptsports:
	#readFromSerial.StartRead(ptsports[0],115200)
