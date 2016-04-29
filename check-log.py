#!/usr/bin/env python
# -*- coding: utf-8 -*-
__version__ = "0.0.6" 
__author__ = "Pavel Yegorov, Maxim Prokopev" 

import os.path
import time
import datetime

import mailnotify
import settings


log_time = os.path.getmtime(settings.RKN_LOG)

deltas = time.time() - log_time

if (deltas > 3600):
    message = "last acces to log is: "+time.ctime(log_time) +"("+ str(log_time) + ")"
    message = message + "\ncurrent date is: "+time.ctime() +"(" + str(time.time()) +")"
    message = message + "\ndiff is: " + str(deltas)
    mailnotify.sendemail ("Log file outdated", message)

