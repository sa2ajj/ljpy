#! /usr/bin/python

from os.path import expanduser

from livejournal import LiveJournal

if 1:
    user = 'mss'
    password = 'rogazzi'
elif 0:
    user = 'test'
    password = 'test'
else:
    user, password = 'leftaw', 'none'

lj = LiveJournal ('Python-ljpy/0.0.1')

from pprint import pprint

pprint (lj.login (user, password))

if 0:
    pprint (lj.checkfriends (lastupdate = '2002-07-24 00:00:00', mask = 1))
else:
    pprint (lj.getevents_last ())
