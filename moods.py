#! /usr/bin/python

from pprint import PrettyPrinter

class dictm:
    def __init__ (self, **kw):
        self.__dict__.update (kw)

moods =  [{'parent': 2, 'id': 1, 'name': 'aggravated'},
           {'parent': 0, 'id': 2, 'name': 'angry'},
           {'parent': 2, 'id': 3, 'name': 'annoyed'},
           {'parent': 46, 'id': 4, 'name': 'anxious'},
           {'parent': 25, 'id': 5, 'name': 'bored'},
           {'parent': 0, 'id': 6, 'name': 'confused'},
           {'parent': 25, 'id': 7, 'name': 'crappy'},
           {'parent': 2, 'id': 8, 'name': 'cranky'},
           {'parent': 25, 'id': 9, 'name': 'depressed'},
           {'parent': 25, 'id': 10, 'name': 'discontent'},
           {'parent': 0, 'id': 11, 'name': 'energetic'},
           {'parent': 2, 'id': 12, 'name': 'enraged'},
           {'parent': 0, 'id': 13, 'name': 'enthralled'},
           {'parent': 74, 'id': 14, 'name': 'exhausted'},
           {'parent': 0, 'id': 15, 'name': 'happy'},
           {'parent': 41, 'id': 16, 'name': 'high'},
           {'parent': 41, 'id': 17, 'name': 'horny'},
           {'parent': 74, 'id': 18, 'name': 'hungry'},
           {'parent': 2, 'id': 19, 'name': 'infuriated'},
           {'parent': 2, 'id': 20, 'name': 'irate'},
           {'parent': 15, 'id': 21, 'name': 'jubilant'},
           {'parent': 25, 'id': 22, 'name': 'lonely'},
           {'parent': 2, 'id': 23, 'name': 'moody'},
           {'parent': 2, 'id': 24, 'name': 'pissed off'},
           {'parent': 0, 'id': 25, 'name': 'sad'},
           {'parent': 53, 'id': 26, 'name': 'satisfied'},
           {'parent': 74, 'id': 27, 'name': 'sore'},
           {'parent': 2, 'id': 28, 'name': 'stressed'},
           {'parent': 74, 'id': 29, 'name': 'thirsty'},
           {'parent': 0, 'id': 30, 'name': 'thoughtful'},
           {'parent': 14, 'id': 31, 'name': 'tired'},
           {'parent': 15, 'id': 32, 'name': 'touched'},
           {'parent': 61, 'id': 33, 'name': 'lazy'},
           {'parent': 74, 'id': 34, 'name': 'drunk'},
           {'parent': 66, 'id': 35, 'name': 'ditzy'},
           {'parent': 66, 'id': 36, 'name': 'mischievous'},
           {'parent': 25, 'id': 37, 'name': 'morose'},
           {'parent': 25, 'id': 38, 'name': 'gloomy'},
           {'parent': 25, 'id': 39, 'name': 'melancholy'},
           {'parent': 14, 'id': 40, 'name': 'drained'},
           {'parent': 15, 'id': 41, 'name': 'excited'},
           {'parent': 26, 'id': 42, 'name': 'relieved'},
           {'parent': 70, 'id': 43, 'name': 'hopeful'},
           {'parent': 15, 'id': 44, 'name': 'amused'},
           {'parent': 0, 'id': 45, 'name': 'determined'},
           {'parent': 0, 'id': 46, 'name': 'scared'},
           {'parent': 2, 'id': 47, 'name': 'frustrated'},
           {'parent': 0, 'id': 48, 'name': 'indescribable'},
           {'parent': 31, 'id': 49, 'name': 'sleepy'},
           {'parent': 31, 'id': 51, 'name': 'groggy'},
           {'parent': 11, 'id': 52, 'name': 'hyper'},
           {'parent': 15, 'id': 53, 'name': 'relaxed'},
           {'parent': 74, 'id': 54, 'name': 'restless'},
           {'parent': 25, 'id': 55, 'name': 'disappointed'},
           {'parent': 6, 'id': 56, 'name': 'curious'},
           {'parent': 53, 'id': 57, 'name': 'mellow'},
           {'parent': 53, 'id': 58, 'name': 'peaceful'},
           {'parent': 11, 'id': 59, 'name': 'bouncy'},
           {'parent': 30, 'id': 60, 'name': 'nostalgic'},
           {'parent': 0, 'id': 61, 'name': 'okay'},
           {'parent': 69, 'id': 62, 'name': 'rejuvenated'},
           {'parent': 64, 'id': 63, 'name': 'complacent'},
           {'parent': 26, 'id': 64, 'name': 'content'},
           {'parent': 64, 'id': 65, 'name': 'indifferent'},
           {'parent': 15, 'id': 66, 'name': 'silly'},
           {'parent': 66, 'id': 67, 'name': 'flirty'},
           {'parent': 53, 'id': 68, 'name': 'calm'},
           {'parent': 15, 'id': 69, 'name': 'refreshed'},
           {'parent': 15, 'id': 70, 'name': 'optimistic'},
           {'parent': 38, 'id': 71, 'name': 'pessimistic'},
           {'parent': 66, 'id': 72, 'name': 'giggly'},
           {'parent': 30, 'id': 73, 'name': 'pensive'},
           {'parent': 25, 'id': 74, 'name': 'uncomfortable'},
           {'parent': 33, 'id': 75, 'name': 'lethargic'},
           {'parent': 33, 'id': 76, 'name': 'listless'},
           {'parent': 53, 'id': 77, 'name': 'recumbent'},
           {'parent': 33, 'id': 78, 'name': 'exanimate'},
           {'parent': 46, 'id': 79, 'name': 'embarrassed'},
           {'parent': 10, 'id': 80, 'name': 'envious'},
           {'parent': 25, 'id': 81, 'name': 'sympathetic'},
           {'parent': 74, 'id': 82, 'name': 'sick'},
           {'parent': 74, 'id': 83, 'name': 'hot'},
           {'parent': 74, 'id': 84, 'name': 'cold'},
           {'parent': 25, 'id': 85, 'name': 'worried'},
           {'parent': 15, 'id': 86, 'name': 'loved'},
           {'parent': 0, 'id': 87, 'name': 'awake'},
           {'parent': 0, 'id': 88, 'name': 'working'},
           {'parent': 88, 'id': 89, 'name': 'productive'},
           {'parent': 88, 'id': 90, 'name': 'accomplished'},
           {'parent': 88, 'id': 91, 'name': 'busy'},
           {'parent': 61, 'id': 92, 'name': 'blah'},
           {'parent': 26, 'id': 93, 'name': 'full'},
           {'parent': 2, 'id': 95, 'name': 'grumpy'},
           {'parent': 66, 'id': 96, 'name': 'weird'},
           {'parent': 82, 'id': 97, 'name': 'nauseated'},
           {'parent': 15, 'id': 98, 'name': 'ecstatic'},
           {'parent': 15, 'id': 99, 'name': 'chipper'},
           {'parent': 28, 'id': 100, 'name': 'rushed'},
           {'parent': 30, 'id': 101, 'name': 'contemplative'},
           {'parent': 0, 'id': 102, 'name': 'nerdy'},
           {'parent': 102, 'id': 103, 'name': 'geeky'},
           {'parent': 2, 'id': 104, 'name': 'cynical'},
           {'parent': 66, 'id': 105, 'name': 'quixotic'},
           {'parent': 66, 'id': 106, 'name': 'crazy'},
           {'parent': 88, 'id': 107, 'name': 'creative'},
           {'parent': 88, 'id': 108, 'name': 'artistic'},
           {'parent': 15, 'id': 109, 'name': 'pleased'},
           {'parent': 2, 'id': 110, 'name': 'bitchy'},
           {'parent': 74, 'id': 111, 'name': 'guilty'},
           {'parent': 2, 'id': 112, 'name': 'irritated'},
           {'parent': 78, 'id': 113, 'name': 'blank'},
           {'parent': 78, 'id': 114, 'name': 'apathetic'},
           {'parent': 102, 'id': 115, 'name': 'dorky'},
           {'parent': 15, 'id': 116, 'name': 'impressed'},
           {'parent': 36, 'id': 117, 'name': 'naughty'},
           {'parent': 45, 'id': 118, 'name': 'predatory'},
           {'parent': 74, 'id': 119, 'name': 'dirty'},
           {'parent': 66, 'id': 120, 'name': 'giddy'},
           {'parent': 15, 'id': 121, 'name': 'surprised'},
           {'parent': 121, 'id': 122, 'name': 'shocked'},
           {'parent': 25, 'id': 123, 'name': 'rejected'},
           {'parent': 25, 'id': 124, 'name': 'numb'},
           {'parent': 15, 'id': 125, 'name': 'cheerful'},
           {'parent': 15, 'id': 126, 'name': 'good'},
           {'parent': 4, 'id': 127, 'name': 'distressed'},
           {'parent': 46, 'id': 128, 'name': 'intimidated'},
           {'parent': 25, 'id': 129, 'name': 'crushed'},
           {'parent': 0, 'id': 130, 'name': 'devious'},
           {'parent': 15, 'id': 131, 'name': 'thankful'},
           {'parent': 15, 'id': 132, 'name': 'grateful'},
           {'parent': 25, 'id': 133, 'name': 'jealous'},
           {'parent': 46, 'id': 134, 'name': 'nervous'}]

class Moods:
    def __init__ (self):
        self.nmoods = {}
        self.children = {}

    def load (self, file):
        try:
            tempo = {}
            execfile (file, tempo)
        except IOError, exc:
            if exc.filename is None:    # arg! execfile() loses filename
                exc.filename = filename
            raise exc

    def save (self, name):
        f = open (name, 'w')

        pp = PrettyPrinter (stream = f, indent = 2)
        f.write ('nmoods = ')
        pp.pprint (self.nmoods)

        f.write ('\nchildren = ')
        pp.pprint (self.children)

        f.close ()
        f = None

    def update (self, moods):
        for mood in moods:
            _mood = dictm (**mood)

            self.nmoods[_mood.id] = (_mood.name, _mood.parent)

            if not self.children.has_key (_mood.parent):
                self.children[_mood.parent] = []

            self.children[_mood.parent].append (_mood.id)

    def dump_mood (self, id, spaces = 1):
        for mood in self.children[id]:
            print ' ' * spaces, mood, self.nmoods[mood][0]

            if self.children.has_key (mood):
                self.dump_mood (mood, spaces + 2)

    def id (self, what):
        pass

m = Moods ()
m.update (moods)
m.dump_mood (0)

m.save ('testing-moods')
