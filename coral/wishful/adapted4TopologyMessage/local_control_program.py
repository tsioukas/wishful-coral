__author__ = "Piotr Gawlowicz"
__copyright__ = "Copyright (c) 2015, Technische Universitat Berlin"
__version__ = "0.1.0"
__email__ = "gawlowicz@tkn.tu-berlin.de"

#Definition of Local Control Program
def my_local_control_program(controller):
	#do all needed imports here!!!
	import time
	import datetime
	from getPTSports import get1stpts
	from readFromSerial import readPort

	print(("\nLC - Name: {}, Id: {} - STARTED".format(controller.name, controller.id)))
    
	@controller.set_default_callback()
	def default_callback2(cmd, data):
		#print(("{} DEFAULT CALLBACK : Cmd: {}, Returns: {}".format(datetime.datetime.now(), cmd, data)))
		#result = controller.radio.iface("wlan0").get_channel()
		#print(("{} Channel is: {}".format(datetime.datetime.now(), result)))
		#controller.send_upstream({"myChannel":result})
		print(("DEFAULT CALLBACK : Cmd: {}, Returns: {}".format(cmd, data)))
		result = "niaaaaaaaaaaaa" #controller.radio.iface("wlan0").get_channel()
		print(("Sending upstream:".format(result)))
		controller.send_upstream({"CtrlMsgRseults":result})
	def callTD(controller):
		#do all needed imports here!!!
		import time
		import datetime
		from getPTSports import get1stpts
		from readFromSerial import readPort
	
	
		#control loop
		while not controller.is_stopped():
			#trying to read from the ACTUAL SERIAL PORT
			ptsPort=get1stpts()
			print ("port found: "+ptsPort)
		
			msg = controller.recv(timeout=1)
			if msg:
				CtrlMsg = msg["CtrlMsg"]
				print("Received:"+CtrlMsg)
			if CtrlMsg=="TD":

				answer=readPort(ptsPort, 115200)

				if  answer: # if answer is not null
					print ("Sending to GC:"+str(answer) )
					controller.send_upstream({"CtrlMsg":answer}) 
			
				# it works fine . send/receive ok
		        
		print(("Local Control Program - Name: {}, Id: {} - STOPPED".format(controller.name, controller.id)))    
                

            #print(("{} Scheduling set channel call with arg: {} in 5 seconds:".format(datetime.datetime.now(), newChannel)))
            #controller.delay(5).radio.iface("wlan0").set_channel(newChannel)
        #else:
        #   print(("{} Waiting for message".format(datetime.datetime.now())))


