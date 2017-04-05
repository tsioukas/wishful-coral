#!/usr/bin/python

import getPTSports
import write2anyPort
import findUSBport


#t1=threading.Thread(target=write2anyPort.writeCont("/dev/pts/4",9600) )

if __name__ == '__main__':

	print ("ptsports:")
	ptsports=getPTSports.getAllpts()
	print ptsports 
	
	print ("USB1 port:")
	print findUSBport.printAll()
	

	for pts in ptsports:
		print ( "write to: " + pts )
		write2anyPort.writeThis(pts, 115200, "msg:" + str(pts))
	
	#write2anyPort.writeThis(ptsports[1], 115200, "msg:" + str(ptsports[1]))	
		#be careful: it will only work with threads !!!
		#write2anyPort.writeCont(pts,115200) 
