#! /usr/bin/python

from livejournal import LiveJournal
from config import Config

config = Config ()
config.load ('lj.conf')

lj = LiveJournal ('Python-ljpy/0.0.1')

from pprint import pprint

info = lj.login (config.username, config.password)

if info.message is not None:
    print 'Server:', info.message

print 'Synchronizing...'

value = lj.syncitems ()

print 'Got information for %d out of %d item(s)' % (value.count, value.total)

for item in value.syncitems:
    print '%s (%s, %s) -- %s (%s)' % (item.item, item.itemid, item.type, item.time, item.action)
