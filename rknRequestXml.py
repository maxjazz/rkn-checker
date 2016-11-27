#!/usr/bin/env python

__author__    = "Maksim Prokopev"
__copyright__ = "(c) 2016, Maksim Prokopev"
__version__   = "0.1"


from lxml import etree as ET
from datetime import datetime,timedelta
import pytz
import lxml
import logging


class rknRequestXML:

	def __init__(self, OperatorName, OperatorINN, OperatorOGRN, OperatorEmail, TimeZone="UTC"):
		self.OperatorName  = OperatorName;
		self.OperatorINN   = OperatorINN;
		self.OperatorOGRN  = OperatorOGRN;
		self.OperatorEmail = OperatorEmail;
		self.TimeZone = TimeZone;

	def sign(self):
		pass


	def generateText(self):
		request = ET.Element('request');

		requestTime = ET.SubElement(request, 'requestTime');
		requestTime.text = datetime.now(pytz.timezone(self.TimeZone)).isoformat();

		requestOperatorName      = ET.SubElement(request, 'OperatorName');
		requestOperatorName.text = self.OperatorName;

		requestOperatorINN = ET.SubElement(request, 'inn');
		requestOperatorINN.text = self.OperatorINN;

		requestOperatorOGRN = ET.SubElement(request, 'ogrn');
		requestOperatorOGRN.text = self.OperatorOGRN;

		requestOperatorEmail = ET.SubElement(request, 'email');
		requestOperatorEmail.text = self.OperatorEmail;

		requestText = lxml.etree.tostring(request, encoding='windows-1251', pretty_print=True, xml_declaration=True)
		#, encoding="windows-1251", pretty_print=True, xml_declaration=True).replace("'",'"').replace('\n','\r\n');
		logging.debug(requestText)

		return str(requestText, 'windows-1251');

	def generate(self, filename):
		text = self.generateText();
		requestFile = open(filename, "w");
		requestFile.write(text);
		requestFile.close();
