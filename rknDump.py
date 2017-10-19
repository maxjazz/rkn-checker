#!/bin/env python

import datetime
import time
import os.path
from xml.etree.ElementTree import ElementTree

import settings


class rknDump:

    def __init__(self, directory):
	self.directory=directory;
	self.updateTime = ""
	self.updateTimeUrgently =  ""
    try:
        DumpFile=ElementTree().parse("/var/log/dump.xml")
    except:
        print ("Could not parses %s /dump.xml" % directory)
    else:
	pass
	#self.updateTime = DumpFile.attrib['updateTime']
	#self.updateTimeUrgently = DumpFile.attrib['updateTimeUrgently']


    def getUpdateTime(self):
	print (self.updateTime)
	#return int(time.mktime(datetime.datetime.strptime(self.updateTime[:19],'%Y-%m-%dT%H:%M:%S').timetuple()))

    def getUpdateTimeUrgently(self):
	print (self.updateTimeUrgently)
	#return int(time.mktime(datetime.datetime.strptime(self.updateTimeUrgently[:19],'%Y-%m-%dT%H:%M:%S').timetuple()))




    def getWebServiceVersion(self):
	webServicePath=self.dir+'dump/webservice'
	if (os.path.isfile(webServicePath)):
	    return open(webServicePath).read()
	else:
            return '0'



    def setWebServiceVersion(self, webserviceversion):
        webServicePath=self.dir+"dump/webservice"
        webService=open(webServicePath, "w")
        webService.write(webserviceversion)
        webService.close()

##########################################################################################


    def setDumpFormatVersion(self, dumpformatversion):
	dumpFormatPath=self.dir+"dump/dumpformat"
	dumpFormat=open(dumpFormatPath,"w")
	dumpFormat.write(dumpformatversion)
	dumpFormat.close()

    def getDumpFormatVersion(self):
        dumpFormatPath=self.dir+"dump/dumpformat"
        if (os.path.isfile(dumpFormatPath)):
            return open(dumpFormatPath).read()
        else:
            return '0'


#############################################################################################

    def setDocVersion(self, docversion):
	docPath=self.dir+"dump/doc"
	doc=open(docPath,'w')
	doc.write(docversion)
	doc.close

    def getDocVersion(self):
	docPath=self.dir+'dump/doc'
	if (os.path.isfile(docPath)):
    	    return open(docPath).read()
    	else:
    	    return '0'




#try:
#    ts=ElementTree().parse(DIR+"dump.xml").attrib['updateTime']
#    dt = datetime.strptime(ts[:19],'%Y-%m-%dT%H:%M:%S')
#    fromFile=int(time.mktime(dt.timetuple()))+3
#except:
#    fromFile=0
