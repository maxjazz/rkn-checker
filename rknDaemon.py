#!/usr/bin/env python3

"""
Disk and Execution Monitor (Daemon)


References:
1) Advanced Programming in UNIX Environment: W Richard Stevens
2) Unix Programming Frequently Asked Questions:
         http://www.erlenstar.demon.co.uk/unix/faq_toc.html

"""

__author__    = "Maksim Prokopev"
__copyright__ = "(c) 2015, 2016 Maksim Prokopev"
__version__   = "0.2"

#Standart Python Library
import os
import sys
import time
import datetime
import logging
#import mailnotify

from xml.etree.ElementTree import ElementTree


#from zapretinfo import ZapretInfo
#from dump import DumpFile


import settings
try:
    DIR = settings.WORK_DIR
except AttributeError:
    DIR = os.getcwd()
    #self.zapretlogger.info("Directory is not defined. Setting to "+DIR)


def sec2hr(sec):
    h = sec//3600
    m = (sec//60)%60
    return '%d hr %02d min'% (h, m)



class rknDaemon:

    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null', refresh=15):
        self.pidfile = pidfile
        self.stdin   = stdin
        self.stdout  = stdout
        self.stderr  = stderr
        self.refresh = refresh
        self.rknlog= logging.getLogger("rkn-%s" % str(os.getpid()))



    def daemonize(self):
        # first fork()
        self.rknlog.debug("First fork staring");
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            self.rknlog.debug("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))
            sys.exit(1)

        # switch off from parent environment
        self.rknlog.debug("Switch off from parent environment");
        os.chdir("/")
        os.umask(0)
        os.setsid()

        # second fork
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            self.rknlog.debug("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))
            sys.stderr.write ("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))
            sys.exit (1)

        os.chdir("/")
        os.umask(0)
        os.setsid()

        sys.stdout.flush()
        sys.stdout.flush()

        si = open(self.stdin, 'r')
        so = open(self.stdout, 'a+')
        se = open(self.stderr, 'a+')

        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdin.fileno())

        # write pidfile
        pid = str(os.getpid())
        open(self.pidfile, "w+").write("%s" % pid)
        self.rknlog.debug("======== Daemonize succes =========")

    def run(self):
        while True:
            #rkndump           = ZapretInfo()
            #DumpDate          = rkndump.getLastDumpDate() 	# Dump timestamp in msec
            #DumpDateUrgently  = rkndump.getLastDumpDateEx() 	# Urgently Dump timestamp im msec
            #WebServiceVersion = rkndump.getWebServiceVersion()  # Web-service string "X.Y"
            #DumpFormatVersion = rkndump.getDumpFormatVersion()  # Dump format version string "X.Y"
            #DocVersion        = rkndump.getDocVersion()         # Doc version string "X.Y"

            #localdump 	      = DumpFile(DIR);
	    #LocalDumpDate     = localdump.getUpdateTime()
	    #LocalDumpDateUrgently = localdump.getUpdateTimeUrgently()

	    #deltaDumpDate = DumpDate/1000 - LocalDumpDate
	    #deltaDumpDateUrgently = DumpDateUrgently/1000 - LocalDumpDateUrgently



            #self.rknlog.info("Dump date:\t\t%s [local: %s, deltas: %s ]"
            #                       % (datetime.datetime.fromtimestamp(DumpDate/1000),
            #                          datetime.datetime.fromtimestamp(LocalDumpDate),
            #                          sec2hr(deltaDumpDate) ))

            #self.rknlog.info("Dump date urgently:\t%s [local: %s, deltas: %s  ]"
            #                       % (datetime.datetime.fromtimestamp(DumpDateUrgently/1000),
            #                          datetime.datetime.fromtimestamp(LocalDumpDateUrgently),
            #                          sec2hr(deltaDumpDateUrgently) ))
            #self.rknlog.info("Web Service Version:\t\t%s [local: %s]" % (WebServiceVersion, localdump.getWebServiceVersion()))
            #self.rknlog.info("Dump Format Version:\t\t%s [local: %s]" % (DumpFormatVersion, localdump.getDumpFormatVersion()))
            #self.rknlog.info("Operator's Doc Version:\t%s [local: %s]" % (DocVersion, localdump.getDocVersion()) )

    	#if (deltaDumpDateUrgently <> 0):
            self.rknlog.info("Need urgently update")
        #    os.system("/home/cmd4jazz/roskomnadzor/download.sh")

    	#if (deltaDumpDate >= 24*60*60 ):
            self.rknlog.info("Need daily update")


            #os.system("/home/cmd4jazz/roskomnadzor/download.sh")


    	#if (WebServiceVersion > localdump.getWebServiceVersion()):
            self.rknlog.info("New Version of Web Service")
            #localdump.setWebServiceVersion(WebServiceVersion)

    	#if (DumpFormatVersion > localdump.getDumpFormatVersion()):
            self.rknlog.info("New Version of Dump Format")
            #localdump.setDumpFormatVersion(DumpFormatVersion)


    	#if (DocVersion > localdump.getDocVersion()):
            self.rknlog.info("New Version of Operator's Doc Version")
            #localdump.setDocVersion(DocVersion)
            #os.system("wget -c http://vigruzki.rkn.gov.ru/docs/description_for_operators_actual.pdf -O /home/cmd4jazz/roskomnadzor/dump/doc-"+DocVersion+".pdf"
            #              " -o /home/cmd4jazz/roskomnadzor/dump/doc-"+DocVersion+".log")
            #message = "New documentation for RosKomNadzor Servise is available ( version "+DocVersion+")\nHave fun!\n---\nrkn-support";
            #mailnotify.sendemail ("New version of RKN service", message, "/home/cmd4jazz/roskomnadzor/dump/doc-"+DocVersion+".pdf")



            time.sleep (self.refresh*60)

            self.rknlog.info ("="*100)

    def start(self):
        self.daemonize()
        self.rknlog.info("="*100 )
        self.rknlog.info("                      Starting daemon with pid: %s", str(os.getpid()) )
        self.rknlog.info("                      Working directory: %s", str(os.getcwd()) )
        self.rknlog.info("="*100 )
        self.run()