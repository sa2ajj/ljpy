#! /usr/bin/python

from os.path import expanduser

from livejournal import LiveJournal

if 1:
    user = 'mss'
    password = 'rogazzi'
elif 0:
    user = 'test'
    password = 'test'
else:
    user, password = 'leftaw', 'none'

lj = LiveJournal ('Python-ljpy/0.0.1')

from pprint import pprint

pprint (lj.login (user, password))
pprint (lj.postevent (unicode ('�������� ����', 'koi8-r'), unicode ('���� ��������� ���������', 'koi8-r')))
