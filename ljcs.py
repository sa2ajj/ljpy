#! /usr/bin/python

from livejournal import LiveJournal, Config, evalue, list2mask
from livejournal.config import std_parser

parser = std_parser (usage = 'Usage: %prog [options]')

parser.add_option ('-F', '--from',
                   action = 'store', type = 'string', dest = 'sfrom', default = 'public',
                   help = 'what security level change', metavar = 'SECURITY')
parser.add_option ('-T', '--to',
                   action = 'store', type = 'string', dest = 'sto', default = 'friends',
                   help = 'what security level change', metavar = 'SECURITY')

options, args = parser.parse_args ()

config = Config ()
config.load (evalue ('~/.ljrc', options.config))

server = config.server

username = evalue (server.username, options.username)
password = evalue (server.password, options.password)

if username is None or password is None:
    print "You must provide both user name and password"
    sys.exit (2)

lj = LiveJournal (config.misc.version)

info = lj.login (username, password)

sfrom = list2mask (options.sfrom, info.friendgroups)
sto = list2mask (options.sto, info.friendgroups)

print 'We are about to change from "%s" to "%s"' % (sfrom, sto)

if 0:
    daycounts = lj.getdaycounts ()['daycounts']

    for day in daycounts:
        # print day['date'], '->', day['count']
        events = lj.getevents ('day', day['date'])

        for event in events:
            security = getattr (event, 'security', 'public')

            if security == 'usemask':
                print security, event.allowmask
            else:
                print security
