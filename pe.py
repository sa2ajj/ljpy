#! /usr/bin/python

from os.path import expanduser

from livejournal import LiveJournal
from config import Config

config = Config ()
config.load ('lj.conf')

lj = LiveJournal ('Python-ljpy/0.0.1')

from pprint import pprint

pprint (lj.login (config.username, config.password))
pprint (lj.postevent (unicode ('�������� ����', 'koi8-r'), unicode ('���� ��������� ���������', 'koi8-r')))
