#! /usr/bin/python

import sys
from os.path import expanduser

from optik import OptionParser

from livejournal import LiveJournal, mdict
from config import Config

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

props = { 'opt_preformatted' : 1 }

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
print lj.postevent (event, subject = subject, props = props)
