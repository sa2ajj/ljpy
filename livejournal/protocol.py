# Copyright (C) 2002 by Mikhail Sobolev <mss@mawhrin.net>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software 
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

'''This is a simple implementation of XML-RPC variant of LiveJournal
client-server protocol as of 
    http://www.livejournal.com/doc/server/ljp.csp.xml-rpc.protocol.html

The method documentation was copied from the appropriate articles.  I am not
that sure that this is really OK.
'''

from xmlrpclib import Server, Binary, binary, Fault
from md5 import md5
from types import StringType, UnicodeType, DictType
import re
from time import time, localtime

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

def listofdict (what):
    return map (lambda x, m = dictm : m (**x), what)

class LiveJournal:
    '''Main interface class

    Instance attributes:
        lj : xmlrpclib.Server
            the class implementing all xml-rpc data conversions and exchange
        clientversion : string
            it's supplied
        username : string
        hpassword : string
            username and password.  if username is None, the user is not
            "logged in", therefore all methods beside 'login' will fail.

            as soon as the user is logged on, the hashed form of the password
            is stored and used from that moment on.
'''

    def __init__ (self, clientversion, base = 'http://www.livejournal.com/interface/xmlrpc', verbose = 0):
        self.lj = Server (base, verbose = verbose)
        self.clientversion = clientversion

        self.user = None
        self.hpassword = None

    def _do_request (self, mode, args):
        method = getattr (self.lj.LJ.XMLRPC, mode)

        return method (args)

    def _required_headers (self, **other):
        args = dictm (ver = 1, clientversion = self.clientversion, **other)

        if self.user is not None:
            args.username = self.user
            args.hpassword = self.hpassword

        return args

    def login (self, user, password):
        '''login - validate user's password and get base information needed for
        client to function

        Login to the server, while announcing your client version. The server
        returns with whether the password is good or not, the user's name, an
        optional message to be displayed to the user, the list of the user's
        friend groups, and other things.'''

        try:
            hpassword = md5 (password).hexdigest ()

            args = self._required_headers (username = user, hpassword = hpassword, getmoods = 134, getpickws = 1, getpickwurls = 1)

            result = self._do_request ('login', args.__dict__)

            self.user = user
            self.hpassword = hpassword

            result['message'] = result.get ('message', None)
            result = dictm (**result)
            result.friendgroups = listofdict (result.friendgroups)
        except Fault:
            self.user = None
            self.hpassword = None

            result = None

        return result

    def postevent (self, event, subject = None, usejournal = None, security = None, when = None, props = None):
        '''postevent - The most important mode, this is how a user actually submits a new log entry to the server.

        Given all of the require information on a post, optioanlly adding
        security or meta data, will create a new entry. Will return the itemid
        of the new post.'''

        if self.user is not None:
            assert type (event) == UnicodeType
            assert subject is None or type (subject) == UnicodeType

            args = self._required_headers (event = event.encode ('utf-8'))

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

            result = self._do_request ('postevent', args.__dict__)
        else:
            result = None

        return result

    def editevent (self):
        '''editevent - Edit or delete a user's past journal entry

        Modify an already created event. If fields are empty, it will delete
        the event.'''

        pass

    def editfriendgroups (self):
        '''editfriendgroups - Edit the user's defined groups of friends.

        Given several optional lists, will add/delete/update/rename the friends
        groups for a user.'''

        pass

    def editfriends (self):
        '''editfriends - Add, edit, or delete friends from the user's friends list.

        Takes up to two lists, one of friends to delete and one of friends to add.
        Several options are allowed to be specified when adding a friend. It
        returns a verbose list of the friends added, if any were.'''

        pass

    def getevents (self):
        raise 'Sorry this function is not implemented in a way as it is described in LJ'

    def _getevents (self, args):
        '''helper function to process what getevents returned'''

        what = self._do_request ('getevents', args.__dict__)

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

    def getevents_last (self, howmany = 20, beforedate = None, usejournal = None, truncate = 3, prefersubject = 0, noprops = 0):
        if self.user is not None:
            # mss: i am not sure that this assert is a really good idea: lj
            # should return an error anyway.
            assert howmany <= 50
            args = self._required_headers (selecttype = 'lastn', howmany = howmany)

            if beforedate is not None:
                args.beforedate = beforedate

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

    def getfriends (self, includefriendof = None, includegroups = None, friendlimit = None):
        if self.user is not None:
            args = self._required_headers ()

            if includegroups is not None and includegroups:
                args.includegroups = 1

            if includefriendof is not None and includefriendof:
                args.includefriendof = 1

            if friendlimit is not None:
                args.friendlimit = friendlimit

            result = self._do_request ('getfriends', args.__dict__)

            if result.has_key ('friends'):
                friends = listofdict (result['friends'])
            else:
                friends = None

            if result.has_key ('friendofs'):
                friendofs = listofdict (result['friendofs'])
            else:
                friendofs = None

            if result.has_key ('friendgroups'):
                friendgroups = listofdict (result['friendgroups'])
            else:
                friendgroups = None

            result = friends, friendofs, friendgroups
        else:
            result = None

        return result

    def friendof (self):
        '''friendof - Returns a list of which other LiveJournal users list this user as their friend.

        Returns a "friends of" list for a specified user. An optional limit of
        returned friends can be supplied.'''

        pass

    def getfriendgroups (self):
        '''getfriendgroups - Retrieves a list of the user's defined groups of friends.

        Retrieves a list of the user's defined groups of friends.'''

        pass

    def getdaycounts (self):
        pass

    def syncitems (self):
        '''syncitems - Returns a list of all the items that have been created or updated for a user.

        Returns a list (or part of a list) of all the items (journal entries,
        to-do items, comments) that have been created or updated on LiveJournal
        since you last downloaded them. Note that the items themselves are not
        returned --- only the item type and the item number. After you get this
        you have to go fetch the items using another protocol mode. For journal
        entries (type "L"), use the getevents mode with a selecttype of
        "syncitems".'''

        pass

    def checkfriends (self, lastupdate = '', mask = 0):
        '''checkfriends - Checks to see if your friends list has been updated since a specified time.

        Mode that clients can use to poll the server to see if their friends
        list has been updated. This request is extremely quick, and is the
        preferred way for users to see when their friends list is updated,
        rather than pounding on reload in their browser, which is stressful on
        the serves.'''

        if self.user is not None:
            args = self._required_headers (lastupdate = lastupdate, mask = mask)

            result = dictm (**self._do_request ('checkfriends', args.__dict__))
        else:
            result = None

        return result

    def consolecommand (self):
        '''consolecommand - Run an administrative command.

        The LiveJournal server has a text-based shell-like admininistration
        console where less-often used commands can be entered. There's a web
        interface to this shell online, and this is another gateway to that.'''

        pass

class Moods:
    '''Helper class to deal with moods.'''
    def __init__ (self):
        self._moods = {}
        self.children = {}
