#! /usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup (
    name = "ljpy",
    version = "0.8.1",
    description = "Module and scripts for working with LiveJournal servers",
    long_description = '''\
This is a simple implementation of XML-RPC variant of LiveJournal client-server
protocol as of 
    http://www.livejournal.com/doc/server/ljp.csp.xml-rpc.protocol.html
''',
    author = "Mikhail Sobolev",
    author_email = "mss@mawhrin.net",
    url = "http://only.mawhrin.net/~mss/thingies/ljpy/",
    packages = ['livejournal'],
    scripts = [ 'ljp.py', 'ljac.py' ],
    license = 'GPL v2'
)

# vim:ts=4:sw=4:noet
