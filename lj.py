#! /usr/bin/python

from os.path import expanduser

from livejournal import LiveJournal
from config import Config

config = Config ()
config.load ('lj.conf')

lj = LiveJournal ('Python-ljpy/0.0.1')

from pprint import pprint

pprint (lj.login (config.username, config.password))

if 0:
    pprint (lj.checkfriends (lastupdate = '2002-07-24 00:00:00', mask = 1))
else:
    pprint (lj.getfriends (includefriendof = 1, includegroups = 1))
