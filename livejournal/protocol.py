#! /usr/bin/python

from xmlrpclib import Server, Binary, binary, Fault
from md5 import md5
from types import StringType, UnicodeType, DictType
import re
from time import time, localtime

from pprint import pprint

_date = re.compile (r'(?P<year>[12][0-9]{3})-(?P<mon>[0-9]{1,2})-(?P<day>[0-9]{1,2}) (?P<hour>[0-9]{1,2}):(?P<min>[0-9]{2})')

def mdict (**kw):
    return kw

class dictm:
    def __init__ (self, **kw):
        self.__dict__.update (kw)

def getdate (when = None):
    if when is None:
        year, mon, day, hour, min, dummy, dummy, dummy, dummy = localtime (time ())

        result = year, mon, day, hour, min
    else:
        match = _date.match (when)

        if not match:
            raise '%s does not match the date specification' % when

        result = match.group ('year'), match.group ('mon'), match.group ('day'), match.group ('hour'), match.group ('min')

    return result

class LiveJournal:
    def __init__ (self, clientversion, verbose = 0):
        self.lj = Server ('http://www.livejournal.com/interface/xmlrpc', verbose = verbose)
        self.clientversion = clientversion

        self.user = None
        self.password = None

    def login (self, user, password):
        try:
            result = self.lj.LJ.XMLRPC.login (mdict (username = user,
                # password = password,
                hpassword = md5 (password).hexdigest (),
                ver = 1,
                clientversion = self.clientversion,
                getmoods = 134,
                # getmenus = 'yes',
                getpickws = '1',
                getpickwurls = '1'
                ))
            self.user = user
            self.password = password
        except Fault:
            result = None

        return result

    def postevent (self, event, subject = None, usejournal = None, security = None, when = None, props = None):
        if self.user is not None:
            assert type (event) == UnicodeType
            assert subject is None or type (subject) == UnicodeType

            args = dictm (username = self.user,
                hpassword = md5 (self.password).hexdigest (),
                ver = 1,
                clientversion = self.clientversion,
                event = event.encode ('utf-8'))

            if subject is not None:
                args.subject = subject.encode ('utf-8')

            if usejournal is not None:
                args.usejournal = usejournal

            if security is None:
                args.security = 'public'
            elif security == 'private':
                args.security = security
            elif security == 'friends':
                args.security = 'usemask'
                args.allowmask = 1
            else:
                args.security = 'usemask'
                args.allowmask = security

            args.year, args.mon, args.day, args.hour, args.min = getdate (when)

            if type (props) is DictType:
                args.props = props  # i do not check if the properties are correct, maybe it's a good idea to do that? :)

            result = self.lj.LJ.XMLRPC.postevent (args.__dict__)
        else:
            result = None

        return result

    def editevent (self):
        pass

    def editfriendgroups (self):
        pass

    def editfriends (self):
        pass

    def getevents (self):
        raise 'Sorry this function is not implemented in a way as it is described in LJ'

        # assert selecttype in [ 'day', 'lastn', 'one', 'syncitems']

    def _getevents (self, args):
        '''helper function to process what getevents returned'''

        what = self.lj.LJ.XMLRPC.getevents (args)

        result = []

        for entry in what['events']:
            item = {}

            for k, v in entry.items ():
                if isinstance (v, Binary):
                    item[k] = v.data
                else:
                    item[k] = v

            result.append (dictm (**item))

        return result

    def getevents_last (self, howmany = 20, before = None, usejournal = None, truncate = 3, prefersubject = 0, noprops = 0):
        if self.user is not None:
            args = mdict (username = self.user,
                hpassword = md5 (self.password).hexdigest (),
                ver = 1,
                clientversion = self.clientversion,
                selecttype = 'lastn',
                howmany = howmany)))

            result = self._getevents (args)
        else:
            result = None

        return result

    def getevents_day (self, day = None, month = None, year = None, usejournal = None, truncate = 3, prefersubject = 0, noprops = 0):
        if self.user is not None:
            result = None
        else:
            result = None

        return result

    def getevent (self, id, usejournal = None, truncate = 3, prefersubject = 0, noprops = 0):
        pass

    def getevents_sync (self, usejournal = None, truncate = 3, prefersubject = 0, noprops = 0):
        pass

    def getfriends (self):
        pass

    def friendof (self):
        pass

    def getfriendgroups (self):
        pass

    def getdaycounts (self):
        pass

    def syncitems (self):
        pass

    def checkfriends (self, lastupdate = '', mask = 0):
        if self.user is not None:
            result = self.lj.LJ.XMLRPC.checkfriends (mdict (username = self.user,
                hpassword = md5 (self.password).hexdigest (),
                ver = 1,
                clientversion = self.clientversion,
                lastupdate = lastupdate,
                mask = mask
                ))
        else:
            result = None

        return result

    def consolecommand (self):
        pass

class Moods:
    def __init__ (self):
        self._moods = {}
        self.children = {}
