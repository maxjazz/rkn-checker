#!/usr/bin/env python
import sys
sys.path.append("settings")

import logging
import settings

from daemon import Daemon


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=settings.RKN_LOG,
                    filemode='a')
                    
rkn = Daemon(settings.RKN_PID)
rkn.start()
