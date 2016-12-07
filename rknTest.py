#!/usr/bin/env python3

import logging

class rknTest:
    def __init__(self, settings):
        self.OPENSSL = settings['OPENSSL'];
        self.CERT    = settings['CERT'];
        logging.debug ("Init Test Module with OPENSSL=%s and CERT=%s", self.OPENSSL, self.CERT);
        pass

    def openssl(self):
        pass

    def cert(self):
        pass
