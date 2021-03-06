from xml.etree.ElementTree import ElementTree
from datetime import datetime,timedelta
import time
import zipfile
import os
import shutil
from base64 import b64decode
from lxml import etree as ET
import logging
import pytz



class rknChecker:
    # TODO Create
    def __init__(self, settings):
        self.OPERATOR_NAME  = settings['OPERATOR_NAME']
        self.OPERATOR_INN   = settings['OPERATOR_INN']
        self.OPERATOR_OGRN  = settings['OPERATOR_OGRN']
        self.OPERATOR_EMAIL = settings['OPERATOR_EMAIL']
        self.WORK_DIR       = settings['WORK_DIR']
        self.DOC_VERSION    = settings['DOC_VERSION']


        logging.debug("Operator name is: %s", self.OPERATOR_NAME)
        logging.debug("Operator INN is: %s", self.OPERATOR_INN)
        logging.debug("Operator OGRN is: %s", self.OPERATOR_OGRN)
        logging.debug("Operator email is: %s", self.OPERATOR_EMAIL)



        logging.debug ("Path for request.xml is: %s", self.WORK_DIR);
        self.XML_FILE_NAME = self.WORK_DIR+"request.xml"
        self.P7S_FILE_NAME = self.WORK_DIR+"request.xml.sign"
        self.DOC_VERSION   = self.DOC_VERSION

    def getDumpDate(self):
        try:
            et = ElementTree().parse(self.WORK_DIR + "dump.xml")
        except IOError:
            logging.debug("Can't find dump.xml");
            return '1970-01-01T00:00:00'
        else:
            ts = et.attrib['updateTime']
            dt = datetime.strptime(ts[:19], '%Y-%m-%dT%H:%M:%S')
            self.DumpDate = int(time.mktime(dt.timetuple())) + 3
            return self.DumpDate

    def getRknDate(self):
        self.RknDate = ZapretInfo().getLastDumpDate()
        return self.RknDate

    def generateRequestXML(self):
        request = ET.Element('request')
        requestTime = ET.SubElement(request, 'requestTime')
        requestTime.text = datetime.now(pytz.utc).isoformat()
        operatorName = ET.SubElement(request, 'operatorName')
        operatorName.text = self.OPERATOR_NAME
        inn = ET.SubElement(request, 'inn')
        inn.text = self.OPERATOR_INN
        ogrn = ET.SubElement(request, 'ogrn')
        ogrn.text = self.OPERATOR_OGRN
        email = ET.SubElement(request, 'email')
        email.text = self.OPERATOR_EMAIL
        tree = ET.ElementTree(request)
        #tree.write(self.XML_FILE_NAME, encoding="windows-1251", pretty_print=True, xml_declaration=True)
        requestText = ET.tostring(request, encoding="windows-1251", pretty_print=True, xml_declaration=True)
        requestFile = open(self.XML_FILE_NAME, "w")
        requestText = str(requestText).replace('\n', '\r\n')
        requestFile.write(requestText)
        requestFile.close()

    def signRequestXML(self):
        os.system(
            "/openssl-gost/bin/openssl smime -sign -in " + self.XML_FILE_NAME + " -out " + self.P7S_FILE_NAME + " -signer keys/letus.pem -outform DER");

    def sendRequest(self):
        opener = ZapretInfo()
        request = opener.sendRequest(self.XML_FILE_NAME, self.P7S_FILE_NAME, self.DOC_VERSION)
