#

import time, os
from pprint import PrettyPrinter

class Config:
    __valid_params = [ 'username', 'password' ]

    def __init__ (self, **kw):
        self.update (kw)

    def update (self, what):
        for k, v in what.items ():
            setattr (self, k, v)

    def __setattr__ (self, name, value):
        if name not in [ self.__valid_params ]:
            raise KeyValue, 'invalid key: %s' % name

        self.__dict__[name] = value

    def load (self, name):
        tempo = {}

        try:
            tempo = {}
            execfile (name, tempo)
        except IOError, exc:
            if exc.filename is None:    # arg! execfile() loses filename
                exc.filename = filename
            raise exc

        for name in self.__valid_params:
            if tempo.has_key (name):
                setattr (self, name, tempo[name])

    def save (self, name):
        output = open (name + '.new', 'w')

        output.write ('# This file was automagically generated on: %s\n\n' % time.asctime ())

        names = self.__dict__.keys ()
        names.sort ()

        pp = PrettyPrinter (stream = output, indent = 2)

        for name in names:
            output.write ('%s = ' % name)
            pp.pprint (getattr (self, name))
            output.write ('\n')
