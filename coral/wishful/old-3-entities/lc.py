__author__ = "George Violettas, Tryfon Theodorou"
__copyright__ = "Copyright (c) 2016, University of Macedonia, Greece"
__version__ = "1.0.0"
__email__ = "georgevio@gmail.com, tryfonthe@gmail.com"


#Definition of Local Control Program
def coral_lc(controller):
    #do all needed imports here!!!
	import time
	import datetime
	from write2anyPort import writeThis
	from readFromSerial import StartRead, readPort,StartReadThread
	from getPTSports import get1stpts
	from findUSBport import getZotecUSB
	 

	# Remember: this method is called automatically when this "program" is called by the GC
	@controller.set_default_callback()
	def default_callback(cmd, data):
		print(("{} DEFAULT CALLBACK : Cmd: {}, Returns: {}".format(datetime.datetime.now(), cmd, data)))
		print ("Reading from serial port: "+ptsPort)
		print("this is the set_default_callback method print...")

		# example of a UPI call logic
		#result = controller.radio.iface("wlan0").get_channel()


# ????????????????????????????????????????????????????????????????????????????????????????

# how do we call this ??????????
# for the moment, it is NOT WORKING !!!!!
#====== Reading from UART (Serial port) and send it to GC ==========================
		#answer=readPort(ptsPort, 115200)
		#if  answer:
		#	print ("Sending to GC:"+str(answer) )
		#	controller.send_upstream({"myChannel":answer})    
#==================================================================================			    


#====== Serial Port Discovery (Contiki, Cooja, etc.) =================================
	times2print=1
	portOk = False
	port2RW=False # just a default value for the port 
	
	print("Looking for UART ports...")
	while not port2RW:
		try:
			ptsPort=get1stpts()
			if ptsPort:
				#portOk=True
				port2RW=ptsPort
				break
		except Exception as e:
			#print ("\npts Problem: "+str(e))
			try: # no pts found, looking for USB port				
				usbPort=getZotecUSB()
				if  (usbPort!=100):
					#portOk=True
					port2RW=usbPort
					break
			except Exception as e:
				print("usb search problem:"+str(e) )	
		if times2print%40==0 or times2print==1: # just prints less error messages	
			print ("\nNo port found. Will retry every 5 secs, 4 ever")	
		time.sleep(5) 
		times2print+=1
#====================================================================================

	# BE CAREFUL: This message sould be printed ONLY ONCE (One thread only...)
	print(("\nLC- Name: {}, Id: {} - STARTED".format(controller.name, controller.id)))
		
	# Controlling the on screen waiting messages to print only once...
	printMsgWaiting = True #just filtering too many waiting messages
	printUARTAnswer = True

#====== Reading from UART (Serial port) and send it to GC ==========================			
	try:
		StartReadThread(port2RW, 115200, controller)	
	except Exception as e:
		print ("UART read error: "+str(e))
#====================================================================================


	#control loop
	while not controller.is_stopped():

#==== Waiting to receive from GC (4 ever): this is a non blocking call ===========
		receivedMsg = controller.recv(timeout=1)
		if (receivedMsg):
			Msg = str(receivedMsg["Msg"])         
			#print ("\nOOOUPS ! A MESSAGE JUST ARRIVED FROM GC: " + Msg) 
#===================================================================================

#=========== Write to UART - Serial  Port: pts OR USB !!!! ========================= 
			try:
				writeThis(port2RW,115200,Msg ) # \n will be added by the function
			except Exception as e:
				print ("UART problem: "+str(port2RW)+" "+str(e) )	#====================================================================================
	 
			printMsgWaiting =True # just prints less error messages
		else:
			if printMsgWaiting: 
				print("LC: Waiting for message from GC")# It will print this only once
				printMsgWaiting = False 


      		   
	print(("Local Control Program - Name: {}, Id: {} - STOPPED".format(controller.name, controller.id)))
