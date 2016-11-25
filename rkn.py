#!/usr/bin/env python3
import sys
import logging
import os
import re
import argparse

#import psutil

sys.path.append("settings")
import settings

from rknDaemon import rknDaemon






logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=settings.RKN_LOG,
                    filemode='a')

def parser():
    rknParser = argparse.ArgumentParser()
    rknSubparser = rknParser.add_subparsers()

    # Start RKN
    start_parser = rknSubparser.add_parser('start', help='Starting daemon')
    start_parser.set_defaults(start = True, func = start)

    # Stop RKN
    stop_parser = rknSubparser.add_parser('stop', help='Stop daemon')
    stop_parser.set_defaults(func = stop)

    # Reload RKN
    reload_parser = rknSubparser.add_parser('reload', help='reload daemon')
    reload_parser.set_defaults(func = reload)

    # Show status of RKN
    status_parser = rknSubparser.add_parser('status', help='Show status')
    status_parser.set_defaults(func = status)

    return rknParser

def start():
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

def stop():
    print ("Stop")

def reload():
    print ("Reload")

def status():
    print ("Status")

if __name__ == "__main__":

    rknArgs = parser().parse_args()

    if len(sys.argv) == 1:
        start()
    else:
        rknArgs.func()
    
