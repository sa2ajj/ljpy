#! /usr/bin/python

import sys
from os.path import expanduser

from locale import getdefaultlocale
from optik import OptionParser

from livejournal import LiveJournal, mdict, Config, list2mask

lang, enc = getdefaultlocale ()

parser = OptionParser ()
parser.add_option ('-u', '--username', type='string', dest='username', default = None,
                   help = 'specify username, otherwise the one from the configuration file is used',
                   metavar = 'USER')
parser.add_option ('-p', '--password', type='string', dest='password', default = None,
                   help = 'specify password, otherwise the one from the configuration file is used',
                   metavar = 'PASSWORD')
parser.add_option ('-C', '--config', type='string', dest='config', default = 'lj.conf',
                   help = 'specify config file',
                   metavar = 'CONFIG')
parser.add_option ('-e', '--encoding', type='string', dest='encoding', default = enc,
                   help = 'specify character encoding',
                   metavar = 'ENCODING')
parser.add_option ('-j', '--journal', type='string', dest='journal', default = None,
                   help = 'specify the journal to post to',
                   metavar = 'JOURNAL')
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
parser.add_option ('-P', '--preformatted',
                   action = 'store_true', dest = 'preformatted',
                   help = 'consider the item to be preformatted', default = 0)

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

props = {}

if options.preformatted:
    props['opt_preformatted'] = 1

if options.mood is not None:
    props['current_mood'] = options.mood

if options.music is not None:
    props['current_music'] = options.music

config = Config ()
config.load (options.config)

lj = LiveJournal ('Python-ljpy/0.0.1')

info = lj.login (config.username, config.password)
entry = lj.postevent (event, subject = subject, props = props, security = list2mask (options.security, info.friendgroups))

print 'Posted.\nLink to the post: http://www.livejournal.com/talkread.bml?journal=%s&itemid=%s' % (config.username, entry.itemid*256 + entry.anum)
