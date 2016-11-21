#!/usr/bin/env python

__author__    = "Maksim Prokopev"
__copyright__ = "(c) 2016, Maksim Prokopev"
__version__   = "0.1"


from lxml import etree as ET
from datetime import datetime,timedelta
import pytz



class RequestXML:

	def __init__(self, OperatorName, OperatorINN, OperatorOGRN, OperatorEmail):
		self.OperatorName  = OperatorName;
		self.OperatorINN   = OperatorINN;
		self.OperatorOGRN  = OperatorOGRN;
		self.OperatorEmail = OperatorEmail;
		self.filename = "request.xml";

	def sign(self):
		pass


	def generateText(self):
		request = ET.Element('request');

		requestTime = ET.SubElement(request, 'requestTime');
		requestTime.text = datetime.now(pytz.utc).isoformat();

		requestOperatorName      = ET.SubElement(request, 'OperatorName');
		requestOperatorName.text = self.OperatorName;

		requestOperatorINN = ET.SubElement(request, 'inn');
		requestOperatorINN.text = self.OperatorINN;

		requestOperatorOGRN = ET.SubElement(request, 'ogrn');
		requestOperatorOGRN.text = self.OperatorOGRN;

		requestOperatorEmail = ET.SubElement(request, 'email');
		requestOperatorEmail.text = self.OperatorEmail;

		requestText = ET.tostring(request, encoding="windows-1251", pretty_print=True, xml_declaration=True).replace("'",'"').replace('\n','\r\n');

		return requestText;

	def generate(self):
		text = self.generateText();
		requestFile = open(self.filename, "w");
		requestFile.write(text);
		requestFile.close();
