#! /usr/bin/python

from distutils.core import setup

setup (
	name = "ljpy",
	version = "0.1",
	description = "Module and scripts for working with LiveJournal -- http://www.livejournal.com",
	author = "Mikhail Sobolev",
	author_email = "mss@mawhrin.net",
	url = "http://only.mawhrin.net/~mss/lj/",
	py_modules = ['livejournal'],
    scripts = [ 'ljp.py', 'ljac.py' ]
)
