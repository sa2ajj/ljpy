#! /usr/bin/python

'''this file is a sandbox for my experiments with differrent methods
of the LiveJournal protocol.  Though I include this file in the distribution
it should rather be used as an example...  Misha'''

from livejournal import LiveJournal, Config

config = Config ()
config.load ('~/.ljrc')

server = config.server

lj = LiveJournal (config.misc.version)

from pprint import pprint

pprint (lj.login (server.username, server.password))

if 0:
    pprint (lj.checkfriends (lastupdate = '2002-07-24 00:00:00', mask = 1))
elif 0:
    pprint (lj.getfriends (includefriendof = 1, includegroups = 1))
else:
    print 'Synchronizing...'

    value = lj.syncitems ()

    print 'Got information for %d out of %d item(s)' % (value.count, value.total)

    for item in value.syncitems:
        print '%s (%s, %s) -- %s (%s)' % (item.item, item.itemid, item.type, item.time, item.action)
