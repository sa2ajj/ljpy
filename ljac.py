#! /usr/bin/python

from os.path import expanduser

from livejournal import LiveJournal
from config import Config

config = Config ()
config.load ('lj.conf')

lj = LiveJournal ('Python-ljpy/0.0.1')

from pprint import pprint

info = lj.login (config.username, config.password)

if info.message is not None:
    print 'Message from server:', info.message

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

execute (['friend list'])
