#!/usr/bin/python


# Usage: ./simple arg1
# In ONL/EC2: arg1 = proxy address, for example: 192.168.6.2:8080
# In Cloudfront: arg1 = playlist address, for example http://cse.wustl.edu/~yuanh/streaming/mystream.m3u8


import sys
import getopt
import time
import subprocess
import urllib2
import os

debug = 0
cloudfront = 1

def fetch(PLAYLIST):
	global table
	global PROXY

	output = urllib2.urlopen(PLAYLIST).read()
	cmd = "curl "

	new = output.split('\n')

	for line in new: 
		# print line
		if line.find('http://') != -1:
			if(debug):
				print line
			index = int((line.split('mystream-')[1]).split('.ts')[0])
			if(debug):
				print index

			if table[index] == 0:
				proxy_cmd = ""
				# configure the video segment addresses
				if cloudfront == 0:
					proxy_cmd = cmd + PROXY + "/streaming" + line.split("/streaming")[1]
					
				else :
					proxy_cmd = cmd + line

				print "\n====== " + proxy_cmd				
				os.system(proxy_cmd +  " >> video")
				table[index] = 1;

		if line.find('EXT-X-ENDLIST') != -1:
			exit(1)
	# import pdb; pdb.set_trace()



def main(argv):
	global PROXY
	global PLAYLIST

	print sys.argv[1]

	# debug = 0
 #   	cloudfront = 0
 #   	try:
 #   		opts, args = getopt.getopt(argv,"hcd")
 #   	except getopt.GetoptError:
 #   		print 'simple-fetch.py -c -d'
 #      	sys.exit(2)

	# print "hello"


 #  	print opts

 #  	for opt, arg in opts:
 #  		if opt == '-h':
 #  			print 'simple-fetch.py -d -c'
 #         	sys.exit()
 #        if opt == '-c':
 #         	cloudfront = 1
 #         	print "cloudfront = 1"
 #      	if opt == '-d':
 #      		debug = 1
 #      		print "debug = 1"

	# print "cloudfront = " + cloudfront
	# print "debug = " + debug

	# main function body
	os.system("rm video")

	if cloudfront == 0:
		PROXY = sys.argv[1]
		print "PROXY = " + PROXY
		PLAYLIST = "http://" + PROXY + '/streaming/mystream.m3u8'
	else: 
		PLAYLIST = sys.argv[1]

	print "Playlist = " + PLAYLIST


	while 1:
		fetch(PLAYLIST)
		time.sleep(5)



if __name__ == "__main__":
	PROXY = ""
	PLAYLIST = ""
	table = [0] * 1000
	main(sys.argv[1:])







