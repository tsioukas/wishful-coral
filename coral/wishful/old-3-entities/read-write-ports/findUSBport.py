#!/usr/bin/python

import serial, glob

usbFound = []

usbPorts = []

#search ONLY USB ports..... (e.g. look for zolertia )
def getUSBPort():    
	for usb in glob.glob('/dev/ttyUSB*'): 
		print (usb + " found" )
		usbFound.append(usb)
	
	probePort(usbFound, usbPorts)
	if usbPorts[1]:
		return usbPorts[1] # ATTENTION: returning USB1 where zolertia was found ???

#call this internaly to find all active ports of a specific type   
def probePort(portList, activePorts):        
	for port in portList:
		try:
			s = serial.Serial(port)
			#s.close()
			activePorts.append(port)
			print ( port + " appended" )
		except Exception: 
			pass

def printAll():
	print ("Printing USB ports found, if any:" + "\n" )
	for pt in usbPorts:
		print ("USBPorts: " + str(pt) )

if __name__ == '__main__':
	try:
		port1 = getUSBPort()
		print("Found USB port[1]. Possible zolertia?")
	except Exception as e:
		print("Port not found:"+str(e) )
	printAll()
    
