#!/usr/bin/env python
# -*- coding: utf-8 -*-
__version__ = "0.0.1" 
__author__ = "Maxim Prokopev" 


import smtplib
import sys
from os.path import basename

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



def sendemail (subj, message, files=None):
    from_email = 'maxim@letus.ru'
    to_email = 'sute@letus.ru'
    mypass = 'mobile2'

    msg = MIMEMultipart()
    msg['From'] = 'rkn-support@letus.ru'
    msg['To'] = to_email
    msg['Subject'] = subj
    body = message

    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    if (files != None):
	with open(files, "rb") as fil:
	    msg.attach (MIMEApplication(fil.read(), Content_Disposition = 'attachment; filename="%s"' % basename(files), Name = basename(files)))




    server = smtplib.SMTP('mail.letus.ru')
    server.login(from_email, mypass)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()












