#!/usr/bin/python
try: 
	f = open("??? statistics_1sink_10static_4mob_IminAll12_.dat","r")
	file2write = open("?? statsMobImin12.dat","r+")
	for line in f:
		#if ( line.startswith('1 ') or line.startswith('2 ') or line.startswith('3 ') or line.startswith('4 ') or line.startswith('#')  ):
		if(line.find("PDR with STATIONS' send statistics: ")
			file2write.write(line)
	file2write.truncate()
	
	f.close()
	file2write.close()
	
except Exception as (e):
	print("file not found...")
	



