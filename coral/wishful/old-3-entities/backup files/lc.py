__author__ = "Piotr Gawlowicz"
__copyright__ = "Copyright (c) 2015, Technische Universitat Berlin"
__version__ = "0.1.0"
__email__ = "gawlowicz@tkn.tu-berlin.de"

#@controller.set_default_callback()
#def default_callback(controller):
#	print(("\nLC: {},Id: {}-STARTED".format(controller.name, controller.id)))

	
def write2Serial(controller):

	#do all needed imports here!!!
	import time
	import datetime
	from write2anyPort import writeThis
	from getPTSports import get1stpts
	
	ptsPort=get1stpts()

		
	#while True:
	if not controller.is_stopped():#this is the LC???
		
		gcMsg = controller.recv(timeout=1)
		if gcMsg: #gcMsg is an array of two fields tuples
			#msg2print = gcMsg["msgName"]#multifields messages
			print("LC: received msg. GC says: {}".format(gcMsg) )

			if str(gcMsg)=="TD":
				print ("Msg was Topology Discovery")
				print("I will send it to serPort:"+ptsPort)
				#send to UART port 
				#writeThis(ptsPort,115200, "TD\n" )
			else:
				print("A msg was received...")
				#writeThis(ptsPort,115200, str(gcMsg)+"\n" )

	print("finished writing the message to UART port")			
						
	
	
	
	#controller.stop()  
	#print(("LC: {}, Id: {} - STOPPED".format(controller.name, controller.id)))  
				
def readFromSerial(controller):
	#do all needed imports here!!!
	import time
	import datetime
	from readFromSerial import readPort
	from getPTSports import get1stpts

	ptsPort=get1stpts()
	print ("Reading from serial port: "+ptsPort)

	print(("LC: {}, Id: {} - STARTED".format(controller.name, controller.id))) 
	 
	while  True:
		if not controller.is_stopped():
			msgTag="CtrlMsg"

			answer=readPort(ptsPort, 115200)
			if  answer:
				print ("Sending to GC:"+str(answer) )
				#controller.send_upstream({msgTag:str(answer)})#send to GC
				controller.send_upstream(str(answer) )
			#else:
			#	print ("no GC contact. Sleep for 5s...")
			#	time.sleep(5)
					
	#controller.stop()  
	#print(("LC: {}, Id: {} - STOPPED".format(controller.name, controller.id)))  
			
