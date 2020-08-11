#!/usr/bin/python

from sys import argv
import os
import math
import urllib2
import random
import os.path
import threading

def download_url(baseUrl, zoom, xtile, ytile):
	# Switch between otile1 - otile4
	subdomain = random.randint(1, 4)

	dateCode = baseUrl[:baseUrl.index("/{z}/{x}/{y}")]
	dateCode = dateCode[dateCode.rfind("/")+1:]

	url =  baseUrl.replace("{z}", str(zoom)).replace("{x}", str(xtile)).replace("{y}", str(ytile))
	dir_path = "tiles/%s/%d/%d/" % (dateCode, zoom, xtile)
	download_path = "tiles/%s/%d/%d/%d.png" % (dateCode, zoom, xtile, ytile)
	
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)
	
	if(not os.path.isfile(download_path)):
		#print "downloading %r" % url
		source = urllib2.urlopen(url)
		content = source.read()
		source.close()
		destination = open(download_path,'wb')
		destination.write(content)
		destination.close()
	else: 
		pass
		#print "skipped %r" % url

def downloadDate(date):
	#print("Downloading date %s" % date)
	for zoom in range(0,5):
		for x in range(0, pow(2,zoom)):
			for y in range(0, pow(2,zoom)):                
				download_url(date, zoom, x, y)



def main():
	# Get time references
	source = urllib2.urlopen("https://maps.s5p-pal.com")
	content = source.read()
	source.close()
	
	token = "var l3layers = ["
	content = content[content.index(token)+len(token):]
	content = content[:content.index("];")]
	senseDatesRaw = content.split("L.tileLayer(")
	senseDates = []
	for rL in senseDatesRaw:
		sensingDate = rL.strip()
		if sensingDate != "":
			senseDates.append(sensingDate.split(",")[0][1:-1])

	for date in senseDates:
		th = threading.Thread(target=downloadDate, args=[date])
		th.start()
	
main()    
