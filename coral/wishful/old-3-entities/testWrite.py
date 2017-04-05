#!/usr/bin/python

import serial
from getPTSports import get1stpts  
from write2anyPort import writeThis

ptsPort=get1stpts()

try:
	writeThis(ptsPort, 115200, "Test pts")
	writeThis('dev/ttyUSB0', 115200, "Test USB")
except Exception as e:
	print ("Write exception: "+str(e) )
