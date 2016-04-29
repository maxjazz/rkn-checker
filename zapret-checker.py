#!/usr/bin/env python2
# -*- coding: utf-8 -*-


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



import settings
import mailnotify

try:
    OPERATOR_NAME  = settings.OPERATOR_NAME
    OPERATOR_INN   = settings.OPERATOR_INN
    OPERATOR_OGRN  = settings.OPERATOR_OGRN
    OPERATOR_EMAIL = settings.OPERATOR_EMAIL
except AttributeError:
    print ("Error Inintializing Operator")
    exit ()

try:
    DIR = settings.DIR
except AttributeError:
    DIR = os.getcwd()
    print ("Directory is not defined. Setting to "+DIR)


XML_FILE_NAME = DIR+"request.xml"
P7S_FILE_NAME = DIR+"request.xml.sign"





#Если файлик ранее выгружался, то пробуем получить из него данные
try:
    ts=ElementTree().parse(DIR+"dump.xml").attrib['updateTime']
    dt = datetime.strptime(ts[:19],'%Y-%m-%dT%H:%M:%S')
    fromFile=int(time.mktime(dt.timetuple()))+3
except:
    fromFile=0

opener=ZapretInfo()
#print opener.sendRequest(XML_FILE_NAME,P7S_FILE_NAME)


#Проверяем, изменился ли файлик


fromServer = opener.getLastDumpDate()
logger = open (DIR+"log.txt", 'a');
logger.write( 'Opener get time %d\n' % (fromServer/1000) )
logger.write( 'File get a time %d\n' % (fromFile))
if opener.getLastDumpDate()/1000 <> fromFile:
    #Файлик изменился.Создаем XML-запрос.
    request = ET.Element('request')
    requestTime = ET.SubElement(request, 'requestTime')
    requestTime.text =datetime.now(pytz.utc).isoformat()
    operatorName = ET.SubElement(request, 'operatorName')
    operatorName.text = OPERATOR_NAME
    inn = ET.SubElement(request, 'inn')
    inn.text = OPERATOR_INN
    ogrn = ET.SubElement(request, 'ogrn')
    ogrn.text = OPERATOR_OGRN
    email = ET.SubElement(request, 'email')
    email.text = OPERATOR_EMAIL
    tree = ET.ElementTree(request)
    #tree.write(XML_FILE_NAME, encoding="windows-1251", pretty_print=True, xml_declaration=True)
    requestText = ET.tostring(request, encoding="windows-1251", pretty_print=True, xml_declaration=True).replace("'", '"')
    requestFile = open(XML_FILE_NAME, "w")
    requestText = requestText.replace('\n', '\r\n')
    requestFile.write(requestText)
    requestFile.close()
    #print ET.tostring(request, pretty_print=True, xml_declaration=True)


    #подписываем XML-запрос
    os.system("/openssl-gost/bin/openssl smime -sign -in "+XML_FILE_NAME+" -out "+P7S_FILE_NAME+" -signer keys/letus.pem -outform DER");



    #Отправляем запрос на выгрузку
    request=opener.sendRequest(XML_FILE_NAME,P7S_FILE_NAME,"2.1")
    #Проверяем, принят ли запрос к обработке
    if request['result']:
        #Запрос не принят, получен код
        code=request['code']
        logger.write ( 'Got code %s \n' % (code))
        logger.write ( 'Trying to get result...\n')
        while 1:
            #Пытаемся получить архив по коду
            request=opener.getResult(code)
            if request['result']:
                #Архив получен, скачиваем его и распаковываем
                logger.write( 'Got it!\n' )
                file = open('result.zip', "wb")
                file.write(b64decode(request['registerZipArchive']))
                file.close()
                
                shutil.copyfile('dump.xml', 'old/dump.xml.'+str(int(time.time())))

                zip_file = zipfile.ZipFile("result.zip", 'r')
                zip_file.extract("dump.xml", '')
                zip_file.close()
                break
            else:
                #Архив не получен, проверяем причину.
                if request['resultComment']=='запрос обрабатывается':
                    #Если это сообщение об обработке запроса, то просто ждем минутку.
                    logger.write( 'Not ready yet.\n')
                    time.sleep(60)
                else:
                    #Если это любая другая ошибка, выводим ее и прекращаем работу
                    #print(request['resultComment'])
                    logger.write( 'Error: %s\n' % request['resultComment'])
                    mailnotify.sendemail('Error Update', request['resultComment'])
                    break
    else:
        #Запрос не принят, возвращаем ошибку
        print (request['resultComment'])
        logger.write( 'Error: %s\n' % request['resultComment'])
else:
    logger.write ('No updates\n')

logger.close();