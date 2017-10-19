#!/usr/bin/env python3
import os


try:
  from lxml import etree
except ModuleNotFoundError:
  print ("Can not find lxml module")
  print ("Installing module")
  os.system ("pip3 install lxml")
  from lxml import etree

def printUrgencyType(urgency):
  answer=""
  if (urgency == "1"):
    answer = "Высокая срочность (Незамедлительное реагирования)"
  else:
    answer = "Обычная срочность (24 часа)"

  print ("Urgency Type:", answer)


def printEntryType(entryType):
  answer=""
  if (entryType == "1"):
    answer = "реестр ЕАИС"
  if (entryType == "2"):
    answer = "реестр НАП"
  if (entryType == "3"):
    answer = "реестр 398-ФЗ"
  if (entryType == "4"):
    answer = "реестр 97-ФЗ (организаторы распространения информации)"
  if (entryType == "5"):
    answer = "реестр НАП, постоянная блокировка сайтов"
  if (entryType == "6"):
    answer = "реестр нарушителей прав субъектов персональных данных"

  print ("Entry Type:", answer)


tree = etree.parse('dump.xml')
contents = tree.xpath('//content')


for content in contents:
  print ("============================")
  print ("ID = ",           content.attrib['id'])
  print ("Include Time = ", content.attrib['includeTime'])

  try:
    printUrgencyType(content.attrib['urgencyType'])
  except:
    printUrgencyType("0")

  printEntryType (content.attrib['entryType'])

  try:
    print("Block Type = ", content.attrib['blockType'])
  except:
    print ("No Block Type")

  print("Hash = ", content.attrib['hash'])

  for decisions in content.xpath('decision'):

    print ("Date: ", decisions.attrib['date'])
    print ("Number: ", decisions.attrib['number'])
    print ("Organisation: ", decisions.attrib['org'])

  for domains in content.xpath('domain'):
    print ("Domain: ", domains.text)

  for urls in content.xpath('url'):
    print ("Url: ", urls.text)

  for ips in content.xpath('ip'):
    print ("IP:", ips.text)

  for ipsubnets in content.xpath('ipsubnet'):
    print ("IP Subnet:", ipsubnets.text )




