#! /usr/bin/python

import sys
from locale import getdefaultlocale
from optik import OptionParser

from livejournal import LiveJournal, list2mask, Config, evalue
from livejournal.config import std_parser
from livejournal.convert import args2text
from livejournal.edit import do_edit

lang, enc = getdefaultlocale ()

parser = std_parser (usage = '%prog [options] [message text with spaces]')

parser.add_option ('-e', '--encoding', type='string', dest='encoding', default = None,
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
parser.add_option ('-o', '--options',
                   action = 'store', type = 'string', dest = 'options', default = None,
                   help = 'list of options for the entry')

options, args = parser.parse_args ()

if len (args) > 0:
    event = ' '.join (args)
else:
    event = sys.stdin.read ()

if options.subject is not None:
    subject = options.subject
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
config.load (evalue ('~/.ljrc', options.config))

server = getattr (config, options.server)

lj = LiveJournal (config.misc.version)

info = lj.login (server.username, server.password)

if 0:
    if subject is not None:
        subject = unicode (subject, 'koi8-r')

    event = unicode (event, 'koi8-r')

    entry = lj.postevent (event,
                subject = subject,
                props = props,
                security = list2mask (options.security, info.friendgroups))

    print 'Posted.\nLink to the post: http://www.livejournal.com/talkread.bml?journal=%s&itemid=%s' % (server.username, entry.itemid*256 + entry.anum)
else:
    sys.stdout.write (args2text (info = info, event = event, subject = subject, props = props, security = options.security))
