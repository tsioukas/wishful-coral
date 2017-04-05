#!/usr/bin/python

from readFromSerial import StartRead, readPort
from getPTSports import get1stpts

#while True:
ptsPort=get1stpts()
#print ("port: "+ptsPort)
while True:
	#print ("start listening on port: "+str(ptsPort) )
	answer=readPort(ptsPort, 115200)
	if  answer:
		print ("answer:"+str(answer) )
	#print ("END listening on port: "+str(ptsPort) )
