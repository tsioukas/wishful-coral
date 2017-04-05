#!/usr/bin/python

import threading
import time


class printThread (threading.Thread):
    #def __init__(self, threadID, name, printMsg):
    def __init__(self, printMsg):
        threading.Thread.__init__(self)
        #self.threadID = threadID
        #self.name = name
        #self.printMsg = printMsg
    def run(self):
        #print ("Starting " + self.name)
        print(self.printMsg)
        #print ("Exiting " + self.name)

"""        
# Create new threads
thread1 = printThread(1, "Thread-1", 1)
thread2 = printThread(2, "Thread-2", 2)

# Start new Threads
thread1.start()
thread2.start()
"""
