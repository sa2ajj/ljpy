#! /usr/bin/python

import sys
from os.path import expanduser

from optik import OptionParser

from livejournal import LiveJournal, mdict
from config import Config

specials = [ 'public', 'private', 'friends' ]

def s2s (arg, groups):
    gg = map (lambda x : x.lower (), arg.split (','))

    for special in specials:
        if special in gg:
            gg = special
            break

    if gg in specials:
        security = gg
    else:
        mask = 0

        for group in groups:
            if group.name in gg:
                mask |= (1 << group.id)

        security = str (mask)

    return security

parser = OptionParser ()
parser.add_option ('-s', '--subject',
                   action = 'store', type = 'string', dest = 'subject', default = None,
                   help = 'specify a subject for the event',
                   metavar = 'SUBJECT')
parser.add_option ('-m', '--mood',
                   action = 'store', type = 'string', dest = 'mood', default = None,
                   help = 'tell them what mood you are in',
                   metavar = 'MOOD')
parser.add_option ('-M', '--music',
                   action = 'store', type = 'string', dest = 'music', default = None,
                   help = 'tell them what music you are listening to',
                   metavar = 'MUSIC')
parser.add_option ('-S', '--security',
                   action = 'store', type = 'string', dest = 'security', default = 'public',
                   help = 'restrict access to the item',
                   metavar = 'SECURITY')

options, args = parser.parse_args ()

if len (args) > 0:
    event = ' '.join (args)
else:
    event = sys.stdin.read ()

event = unicode (event, 'koi8-r')

if options.subject is not None:
    subject = unicode (options.subject, 'koi8-r')
else:
    subject = None

if 0:
    props = { 'opt_preformatted' : 1 }
else:
    props = { }

if options.mood is not None:
    props['current_mood'] = options.mood

if options.music is not None:
    props['current_music'] = options.music

if 0:
    print '''subject: %s
props: %s
event:
%s''' % (subject, props, event)

config = Config ()
config.load ('lj.conf')

lj = LiveJournal ('Python-ljpy/0.0.1')

lj.login (config.username, config.password)
print lj.postevent (event, subject = subject, props = props, security = s2s (options.security))
