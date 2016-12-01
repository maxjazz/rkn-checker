#!/usr/bin/env python3
import sys
import logging
import os
import signal
import re
import argparse
import psutil


SETTINGS = {
    'WORK_DIR' : '/var/',
    'RKN_LOG'  : 'rkn-message.log',
    'RKN_PID'  : 'rkn.pid',
    'OPERATOR_NAME' : "OPERATOR",
    'OPERATOR_INN'  : "12345678910",
    'OPERATOR_OGRN' : "12345678910",
    'OPERATOR_EMAIL' : "mail@operator.ru",
    'OPERATOR_TIMEZONE' : "UTC",
    'URL_API'           : 'http://vigruzki.rkn.gov.ru/services/OperatorRequest/?wsdl',
    'DOC_VERSION'       : '2.1'
}


def init ():
    logging.debug ('Load settings from file: settings/settings.py')
    sys.path.append("settings")
    import settings
    SETTINGS['WORK_DIR'] = settings.WORK_DIR
    SETTINGS['RKN_PID']  = settings.RKN_PID
    SETTINGS['RKN_LOG']  = settings.RKN_LOG
    SETTINGS['OPERATOR_NAME'] = settings.OPERATOR_NAME
    SETTINGS['OPERATOR_INN'] = settings.OPERATOR_INN
    SETTINGS['OPERATOR_OGRN'] = settings.OPERATOR_OGRN
    SETTINGS['OPERATOR_EMAIL'] = settings.OPERATOR_EMAIL
    SETTINGS['OPERATOR_TIMEZONE'] = settings.OPERATOR_TIMEZONE
    SETTINGS['URL_API'] = settings.URL_API
    SETTINGS['DOC_VERSION'] = settings.DOC_VERSION



if (os.path.exists('settings/settings.py')):
    init()
else:
    logging.debug ('Can not find setting.py. Loading default')



from rknDaemon import rknDaemon



logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=SETTINGS['WORK_DIR']+SETTINGS['RKN_LOG'],
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
        f = open(SETTINGS['WORK_DIR']+SETTINGS['RKN_PID'], 'r')
    except Exception as e:
        logging.debug ("Error while open file: %s", e)
        rkn = rknDaemon(SETTINGS) #TODO передавать полностью массив в качестве параметра
        rkn.start()
    else:
        pid = f.read();
        if False: #isRunning(pid):
            logging.debug ("RknDaemon is still running with pid = %s", pid);
        else:
            logging.debug ("Process with pid = %s does not exist", pid);
            rkn = rknDaemon(SETTINGS) #TODO передавать полностью массив в качестве параметра
            rkn.start()

def stop():
    try:
        f = open(SETTINGS['WORK_DIR']+SETTINGS['RKN_PID'], 'r');
    except Exception as e:
        logging.debug("Can't find pid file. Nothing to stop.");
        return 1;
    else:
        pid = f.read()

    try:
        os.kill(int(pid), signal.SIGKILL)
    except Exception as e:
        os.remove(SETTINGS['WORK_DIR']+SETTINGS['RKN_PID'])
    else:
        os.remove(SETTINGS['WORK_DIR']+SETTINGS['RKN_PID'])

def restart():
    stop()
    start()

def status():
    try:
        f = open(WORK_DIR+RKN_PID, 'r');
    except Exception as e:
        logging.debug("Can't find pid file. Nothing to stop.");
        print ("Daemon status: not running");
        print ("Settings: ", SETTINGS)
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
