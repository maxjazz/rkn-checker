from xml.etree.ElementTree import ElementTree
from rknChecker import rknChecker
from rknRequestXml import rknRequestXML

#from zapretinfo import ZapretInfo
#from dump import DumpFile

import settings
import logging
import os, sys, time

def sec2hr(sec):
    h = sec//3600
    m = (sec//60)%60
    return '%d hr %02d min'% (h, m)



class rknDaemon:

    def __init__(self, workdir, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null', refresh=15):
        self.workdir = workdir
        self.pidfile = workdir+pidfile
        self.stdin   = stdin
        self.stdout  = stdout
        self.stderr  = stderr
        self.refresh = refresh
        self.rknlog= logging.getLogger("rkn" )



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
        open(self.pidfile, "w+").write("%s" % pid) #TODO: PermissionError: [Errno 13] Permission denied: '/var/rkn.pid'
        self.rknlog.debug("======== Daemonize succes =========")
        self.rknlog= logging.getLogger("rkn-%s" % str(os.getpid()))
        self.rknlog.debug ("Pidfile is: %s", self.pidfile);
    def run(self):
        checker = rknChecker()
        logging.info ("Last dump have a time: %s", checker.getDumpDate());
        request = rknRequestXML(checker.OPERATOR_NAME, checker.OPERATOR_INN, checker.OPERATOR_OGRN, checker.OPERATOR_EMAIL, 'Europe/Moscow' )
        request.generate(self.workdir+'request.xml');
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
