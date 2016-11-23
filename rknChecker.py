from xml.etree.ElementTree import ElementTree
from datetime import datetime,timedelta
from zapretinfo import ZapretInfo
import time
import zipfile
import pytz
import os
import shutil
from base64 import b64decode
from lxml import etree as ET
import logging
import mailnotify
from zapretinfo import ZapretInfo


import settings



class RknChecker:
    # TODO Create
    def __init__(self):
        self.OPERATOR_NAME = settings.OPERATOR_NAME
        self.OPERATOR_INN  = settings.OPERATOR_INN
        self.OPERATOR_OGRN = settings.OPERATOR_OGRN
        self.OPERATOR_EMAIL = settings.OPERATOR_EMAIL

        try:
            self.DIR = settings.DIR
        except AttributeError:
            # Logging about setting dir to current
            self.DIR = os.getcwd()

        self.XML_FILE_NAME = self.DIR+"request.xml"
        self.P7S_FILE_NAME = self.DIR+"request.xml.sign"
        self.DOC_VERSION   = settings.DOC_VERSION

    def getDumpDate(self):
        ts = ElementTree().parse(self.DIR + "dump.xml").attrib['updateTime']
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
        # tree.write(XML_FILE_NAME, encoding="windows-1251", pretty_print=True, xml_declaration=True)
        requestText = ET.tostring(request, encoding="windows-1251", pretty_print=True, xml_declaration=True).replace(
            "'", '"')
        requestFile = open(self.XML_FILE_NAME, "w")
        requestText = requestText.replace('\n', '\r\n')
        requestFile.write(requestText)
        requestFile.close()

    def signRequestXML(self):
        os.system(
            "/openssl-gost/bin/openssl smime -sign -in " + self.XML_FILE_NAME + " -out " + self.P7S_FILE_NAME + " -signer keys/letus.pem -outform DER");

    def sendRequest(self):
        opener = ZapretInfo()
        request = opener.sendRequest(self.XML_FILE_NAME, self.P7S_FILE_NAME, self.DOC_VERSION)


rkn = RknChecker()
