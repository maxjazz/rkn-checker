#!/usr/bin/env python3
import sys
import logging
import os
import signal
import re
import argparse
import psutil

WORK_DIR = "/var/"
RKN_LOG  = "rkn-messages.log"
RKN_PID  = "rkn.pid"

def init (filename):
    loggihg.debug ('Load settings from file: %s', filename)
    sys.path.append("settings")
    import filename
    WORK_DIR = settings.WORK_DIR
    RKN_LOG  = settings.RKN_LOG



if (os.path.exists('settings/settings.py')):
    init('settings')
else:
    logging.debug ('Can not find setting.py. Loading default')



from rknDaemon import rknDaemon



logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=WORK_DIR+RKN_LOG,
                    filemode='a')





def isRunning(pid):
    if (psutil.Process(int(pid))):
    #if (psutil.Process(int(pid)).status=='running'):
        #if (0): #os.path.exists('/proc/'+pid):
        return True
    else:
        return False



def rknParser():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers()

    # Start RKN
    start_parser = subparser.add_parser('start', help='Starting daemon')
    start_parser.set_defaults(start = True, func = start)

    # Stop RKN
    stop_parser = subparser.add_parser('stop', help='Stop daemon')
    stop_parser.set_defaults(func = stop)

    # Restart RKN
    reload_parser = subparser.add_parser('restart', help='restart daemon')
    reload_parser.set_defaults(func = restart)

    # Show status of RKN
    status_parser = subparser.add_parser('status', help='Show status')
    status_parser.set_defaults(func = status)

    return parser

def start():
    try:
        f = open(settings.WORK_DIR+settings.RKN_PID, 'r')
    except Exception as e:
        logging.debug ("Error while open file: %s", e)
        rkn = rknDaemon(WORK_DIR,RKN_PID)
        rkn.start()
    else:
        pid = f.read();
        if False: #isRunning(pid):
            logging.debug ("RknDaemon is still running with pid = %s", pid);
        else:
            logging.debug ("Process with pid = %s does not exist", pid);
            rkn = rknDaemon(WORK_DIR,RKN_PID)
            rkn.start()

def stop():
    try:
        f = open(WORK_DIR+RKN_PID, 'r');
    except Exception as e:
        logging.debug("Can't find pid file. Nothing to stop.");
        return 1;
    else:
        pid = f.read()

    try:
        os.kill(int(pid), signal.SIGKILL)
    except Exception as e:
        os.remove(WORK_DIR+RKN_PID)
    else:
        os.remove(WORK_DIR+RKN_PID)

def restart():
    stop()
    start()

def status():
    try:
        f = open(WORK_DIR+RKN_PID, 'r');
    except Exception as e:
        logging.debug("Can't find pid file. Nothing to stop.");
        print ("Daemon status: not running");
        return 1;
    else:
        pid = f.read()
        status = str(psutil.Process(int(pid)).status())

        print ("Daemon status:", status)

if __name__ == "__main__":

    rknArgs = rknParser().parse_args()

    if len(sys.argv) == 1:
        start()
    else:
        rknArgs.func()
