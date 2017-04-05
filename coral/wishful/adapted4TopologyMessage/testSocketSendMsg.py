#!/usr/bin/env python3


import sys
import datetime
import logging
import random
import time
import threading

from goodSocksClient import Client # Java Socks CLient

def main():
    
	cl=Client() #Java  client

	cl.start()
	
	time.sleep(5)
	print("slept 4 5")
	#time.sleep(5)
	#print("slept 4 5")
    

if __name__ == "__main__":

	main()
