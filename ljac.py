#! /usr/bin/python
# -*- coding: utf-8 -*-
#

'''A console frontend to the administrative interface of LiveJournal servers.
'''

import readline
from locale import getdefaultlocale

from livejournal import LiveJournal, Config, evalue
from livejournal.config import std_parser

lang, defaultenc = getdefaultlocale ()

parser = std_parser (usage = '%prog [options]')

parser.add_option ('-e', '--encoding', type='string', dest='encoding', default = None,
                   help = 'specify character encoding',
                   metavar = 'ENCODING')

options, args = parser.parse_args ()

encoding = evalue (defaultenc, options.encoding)

config = Config ()
config.load (evalue ('~/.ljrc', options.config))

server = getattr (config, options.server)
ljac = config.ljac

username = evalue (server.username, options.username)
password = evalue (server.password, options.password)

if username is None or password is None:
    print "You must provide both user name and password"
    sys.exit (2)

lj = LiveJournal (config.misc.version)

info = lj.login (username, password)

if info.message is not None:
    for line in info.message.split ('\n'):
        print 'Server:', line

def execute (commands):
    result = lj.consolecommand (commands)

    for i in range (len (result)):
        item = result[i]

        if item.success:
            print 'Success:',
        else:
            print 'Failure:',

        print commands[i]

        for t, l in item.output:
            print '%3.3s: %s' % (t, l)

# execute (['friend list'])
while 1:
    commands = []
    ps = '$ '

    while 1:
        try:
            l = raw_input (ps)
        except EOFError:
            commands = None
            break

        if l == ';':
            break

        if l[-1] == ';':
            commands.append (l[:-1])
            break

        commands.append (l)
        ps = '> '

    if commands is not None:
        execute (commands)
    else:
        print '\nQuitting...'
        break
