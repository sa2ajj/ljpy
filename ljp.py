#! /usr/bin/python

import sys

from locale import getdefaultlocale

from livejournal import LiveJournal, list2list, list2mask, Config, evalue
from livejournal.config import std_parser
from livejournal.convert import args2text, text2args

lang, defaultenc = getdefaultlocale ()

parser = std_parser (usage = 'Usage: %prog [options] [message text with spaces]')

parser.add_option ('-e', '--encoding', type='string', dest='encoding', default = None,
                   help = 'specify character encoding',
                   metavar = 'ENCODING')
parser.add_option ('-j', '--journal', type='string', dest='journal', default = None,
                   help = 'specify the journal to post to',
                   metavar = 'JOURNAL')
parser.add_option ('-S', '--security',
                   action = 'store', type = 'string', dest = 'security', default = 'public',
                   help = 'restrict access to the item', metavar = 'SECURITY')
parser.add_option ('-o', '--options',
                   action = 'store', type = 'string', dest = 'options', default = None,
                   help = 'list of options for the entry')
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
parser.add_option ('-b', '--batch',
                   action = 'store_true', dest = 'batch', default = None,
                   help = 'use in a batch mode: the text will be read from the standard input and posted right away')
parser.add_option ('-i', '--include',
                   action = 'store', dest = 'draft', default = None,
                   help = 'specify the file, which contains the draft of the message (this option is avilable only in non-batch mode)',
                   metavar = 'FILE')

options, args = parser.parse_args ()

# MSS: i may want to be able to specify the encoding from the configuration file
encoding = evalue (defaultenc, options.encoding)

subject = options.subject

if len (args) > 0:
    body = ' '.join (args)
else:
    body = ''

props = {}

if options.options is not None:
    for option in list2list (options.options):
        if option in [ 'preformatted', 'nocomments', 'backdated', 'noemail' ]:
            props['opt_%s' % option] = 1
        else:
            print 'Ignoring unknown option:', option

if options.mood is not None:
    props['current_mood'] = options.mood

if options.music is not None:
    props['current_music'] = options.music

config = Config ()
config.load (evalue ('~/.ljrc', options.config))

server = getattr (config, options.server)
ljp = config.ljp

username = evalue (server.username, options.username)
password = evalue (server.password, options.password)

if username is None or password is None:
    print "You must provide both user name and password"
    sys.exit (2)

usejournal = evalue (None, options.journal)

lj = LiveJournal (config.misc.version)

info = lj.login (username, password)

security = list2mask (options.security, info.friendgroups)

if evalue (None, ljp.batch, options.batch):
    body = body + '\n' + sys.stdin.read ()
else:
    # At this point we have the following variables holding useful information:
    #  -- body
    #  -- subject
    #  -- props
    #  -- usejournal
    #  -- security

    if 0:
        text = args2text (info = info, event = body, usejournal = usejournal, subject = subject, props = props, security = options.security)

        pass #  process the text

        # subject, usejournal, body, props, security = text2args (info, text)

    print 'Sorry, non-batch mode is not supported yet'
    sys.exit (1)

body = unicode (body, encoding)

if subject is not None:
    subject = unicode (subject, encoding)

if props.has_key ('current_mood'):
    props['current_mood'] = unicode (props['current_mood'], encoding)

if props.has_key ('current_music'):
    props['current_music'] = unicode (props['current_music'], encoding)

entry = lj.postevent (body,
                usejournal = usejournal,
                subject = subject,
                props = props,
                security = security)

print 'Posted.\nLink to the post: http://www.livejournal.com/talkread.bml?journal=%s&itemid=%s' % (usejournal or server.username, entry.itemid*256 + entry.anum)
