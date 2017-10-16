#!/usr/bin/env python
# -*- coding: utf-8 -*-
__version__ = "0.0.6" 
__author__ = "Pavel Yegorov, Maxim Prokopev" 


import suds 
from base64 import b64encode 

API_URL = "http://vigruzki.rkn.gov.ru/services/OperatorRequest/?wsdl"

class ZapretInfo:
    def getLastDumpDateEx(self):
	pass
	client = suds.client.Client(API_URL)
	result = client.service.getLastDumpDateEx()
	self.webServiceVersion = result['webServiceVersion']
	self.dumpFormatVersion = result['dumpFormatVersion']
	self.docVersion = result['docVersion']
	self.lastDumpDateUrgently = result['lastDumpDateUrgently']
	return self.lastDumpDateUrgently

    def getDocVersion(self):
	return self.docVersion

    def getWebServiceVersion(self):
	return self.webServiceVersion
	
    def getDumpFormatVersion(self):
	return self.dumpFormatVersion


    def getLastDumpDate(self):
	client = suds.client.Client(API_URL)
	result=client.service.getLastDumpDate()
	return result

    def sendRequest(self,requestFile,signatureFile,docVersion):
	# type: (object, object, object) -> object
	file = open(requestFile, "rb")
	data = file.read()
	file.close()
	xml = b64encode(data)
	file = open(signatureFile, "rb")
	data = file.readlines()
	file.close()
	if '-----' in data[0]:
	    sert = ''.join(data[1:-1])
	else:
	    #sert = ''.join(data)
	    sert = b64encode(''.join(data))
	client = suds.client.Client(API_URL)
	result=client.service.sendRequest(xml,sert,docVersion)
	return dict(((k, v.encode('utf-8')) if isinstance(v, suds.sax.text.Text) else (k, v)) for (k, v) in result)

    def getResult(self,code):
	client = suds.client.Client(API_URL)
	result=client.service.getResult(code)
	return dict(((k, v.encode('utf-8')) if isinstance(v, suds.sax.text.Text) else (k, v)) for (k, v) in result)
