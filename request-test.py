#!/usr/bin/env python

__author__    = "Maksim Prokopev"
__copyright__ = "(c) 2016, Maksim Prokopev"
__version__   = "0.1"


from request import RequestXML

rq_XML = RequestXML("OPERATOR", "12", "12", "12", "Europe/Moscow");
rq_XML.generate("request.xml")
