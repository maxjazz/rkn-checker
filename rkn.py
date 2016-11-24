#!/usr/bin/env python3
import sys
import logging
import os
import re

#import psutil

sys.path.append("settings")
import settings

from rknDaemon import rknDaemon






logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=settings.RKN_LOG,
                    filemode='a')

if __name__ == "__main__":

    # 1. Проверка наличия всех зависимостей
    # 2. Проверка запущенного rknDaemon()
    f = open(settings.RKN_PID, 'r')
    pid = f.read();
    print ('/proc/'+pid);
    print (os.path.exists('/proc/'+pid));
    if os.path.exists('/proc/'+pid):
        logging.debug ("RknDaemon is running now with pid = %s", pid);
    else:
        logging.debug ("Process with pid = %s does not exist", pid);
        rkn = rknDaemon(settings.RKN_PID)
        rkn.start()