#! /usr/bin/python
# -*- coding: utf-8 -*-

from time import strftime, localtime, gmtime
from os.path import expanduser

cdata = lambda x: '<![CDATA[%s]]>' % x

def nicedatetime (what):
    return strftime ("%F %T", localtime (what))

from livejournal import LiveJournal, Config, evalue
from livejournal.config import std_parser

parser = std_parser (usage = '%prog [options]')

parser.add_option ('-f', '--file', type='string', dest='file', default = 'lj.backup',
                   help = 'specify the file to store the backup to',
                   metavar = 'FILE')

options, args = parser.parse_args ()

config = Config ()
config.load (evalue ('~/.ljrc', options.config))

server = getattr (config, options.server)
ljbackup = config.ljbackup

username = evalue (server.username, options.username)
password = evalue (server.password, options.password)

if username is None or password is None:
    print "You must provide both user name and password"
    sys.exit (2)

backupname = evalue (ljbackup.file, options.file)

lj = LiveJournal (config.misc.version)

info = lj.login (username, password)

if info.message is not None:
    print 'Server:', info.message

backup = open (expanduser (backupname), 'w')

print 'Synchronizing...'

value = lj.syncitems ()

print 'Got information for %d out of %d item(s)' % (value.count, value.total)

print >> backup, '''<?xml version='1.0'?>
<events>'''

for item in value.syncitems:
    if item.type == 'L':
        print '%s (%s, %s) -- %s (%s)' % (item.item, item.itemid, item.type, item.time, item.action)

        events = lj.getevent (item.itemid)

        if len (events) == 1:
            event = events[0]

            print >> backup, '<event id="%s" anum="%s" time="%s">' % (event.itemid, event.anum, event.eventtime)
            if hasattr (event, 'subject'):
                print >> backup, '  <subject>%s</subject>' % cdata (event.subject)

            for prop, value in event.props.items ():
                print >> backup, '  <prop name="%s">%s</prop>' % (prop, cdata (value))

            print >> backup, '  <body>%s</body>' % cdata (event.event)
            print >> backup, '</event>'

print >> backup, '</events>'
