"""Classes that define Words."""
from functools import reduce, total_ordering


@total_ordering
class Word(object):
    """Represent a played word."""

    def __init__(self, word, **kwargs):
        """Establish a played word instance."""
        super(Word, self).__init__()
        self._kwargs = kwargs
        self.word = word.strip().upper()
        self.coord = kwargs.get('coord', False)
        self.direction = kwargs.get('direction', False)
        self.player = kwargs.get('player', False)
        self.score = kwargs.get('score', False)
        self.played = False  # if True, word has not been played

    @property
    def x(self):
        if self.coord:
            return self.coord[0]
        return False

    @property
    def y(self):
        if self.coord:
            return self.coord[1]
        return False

    def compute_word_score(self, squares, tilebag):
        """Given word and tile squares, compute the word score."""
        assert len(self.word) == len(squares), "Word doesn't fit error."
        # convert letters to values
        letter_values = [tilebag[letter].value for letter in self.word]
        pair = zip(letter_values, squares)
        ls = []
        wms = []
        wm = 1
        for lv, m in pair:
            if m.tile_multiplier_name == 'triple word':
                wms.append(3)
                ls.append(lv)
            elif (m.tile_multiplier_name == 'double word' or
                  m.tile_multiplier_name == 'center'):
                wms.append(2)
                ls.append(lv)
            elif m.tile_multiplier_name == 'single letter':
                ls.append(lv)
            elif m.tile_multiplier_name == 'double letter':
                ls.append(lv * 2)
            elif m.tile_multiplier_name == 'triple letter':
                ls.append(lv * 3)
        ls = sum(ls)
        if len(wms) > 0:
            wm = reduce((lambda x, y: x * y), wms)
        self.score = (ls * wm)

    def __repr__(self):
        return "wwfs.Word: {}".format(self.word)

    def __str__(self):
        return "word:{} at:{}:{} score:{}".format(self.word, self.coord,
                                                  self.direction, self.score)

    def __hash__(self):
        return hash((self.word, self.coord, self.direction))

    def __baseeq__(self, other):
        return (self.__class__ == other.__class__)

    def __eq__(self, other):
        return (self.__baseeq__(other) and
                (self.score, self.word, self.x, self.y, self.direction) ==
                (other.score, other.word, self.x, self.y, self.direction))

    def __lt__(self, other):
        return (self.__baseeq__(other) and
                (self.score, self.word, self.x, self.y, self.direction) <
                (other.score, other.word, self.x, self.y, self.direction))

    def __le__(self, other):
        return (self.__baseeq__(other) and
                (self.score, self.word, self.x, self.y, self.direction) <=
                (other.score, self.word, self.x, self.y, self.direction))

    def __ne__(self, other):
        return (self.__baseeq__(other) and
                not self.__eq__(other.word))

    def __len__(self):
        """Returns length of word."""
        return len(self.word)

    def __copy__(self):
        newone = type(self)(self.word)
        newone.__dict__.update(self.__dict__)
        return newone


class PlayedWords(object):
    """Represent all played words."""

    def __init__(self, **kwargs):
        """Establish a list of played words."""
        super(PlayedWords, self).__init__()
        self._kwargs = kwargs
        self.words = []

    def get_by_coord(self, xy, direction):
        """Retrieve a word given xy and direction."""
        for word in self:
            if word.coord == xy and word.direction == direction:
                return word

    def __str__(self):
        """Represent played words."""
        return "{} words have been played.".format(len(self.words))

    def __iter__(self):
        """Iterate over all played words."""
        for word in self.words:
            yield word

    def add_word(self, word):
        """Given word coordinates and direction, add it to the played words."""
        self.words.append(word)
