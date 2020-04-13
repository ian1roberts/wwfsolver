"""Classes that define Words."""
from abc import ABC, abstractmethod
from functools import total_ordering


@total_ordering
class BaseWord(ABC):
    """Represent a played word."""

    def __init__(self, word, **kwargs):
        """Establish a played word instance."""
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

    @property
    def letters(self):
        return list(self.word)

    @abstractmethod
    def compute_word_score(self, squares, tilebag):
        """Given a single word and tile squares, compute the word score."""
        assert len(self.word) == len(squares), "Word doesn't fit error."
        # convert letters to values
        letter_values = [tilebag[letter].value for letter in self.word]
        pair = zip(letter_values, squares)
        letter_scores = []
        word_multipliers = []
        for letter_value, square in pair:
            if square.free:
                letter_scores.append(
                                letter_value * square.letter_value_multiplier)
                word_multipliers.append(square.word_value_multiplier)
            else:
                letter_scores.append(letter_value)
                word_multipliers.append(1)

        letter_sum = sum(letter_scores)
        wm_total = 1
        while word_multipliers:
            wm = word_multipliers.pop()
            wm_total *= wm
        self.score = letter_sum * wm_total

    def __repr__(self):
        return "{} {}".format(self.__class__, self.word)

    def __str__(self):
        return "word:{} at:{}:{} score:{}".format(self.word, self.coord,
                                                  self.direction, self.score)

    def __hash__(self):
        return hash((self.word, self.coord, self.direction))

    def __baseeq__(self, other):
        return (self.__class__ == other.__class__)

    def __eq__(self, other):
        return (self.__baseeq__(other) and
                (self.score, self.word) == (other.score, other.word))

    def __lt__(self, other):
        return (self.__baseeq__(other) and
                (self.word == other.word) and (self.word < other.word))

    def __len__(self):
        """Returns length of word."""
        return len(self.word)

    def __copy__(self):
        newone = type(self)(self.word)
        newone.__dict__.update(self.__dict__)
        return newone


class Word(BaseWord):
    """Represent simple words. No extensions, crosses runs."""

    def __init__(self, word, **kwargs):
        super(Word, self).__init__(word, **kwargs)

    def compute_word_score(self, squares, tilebag):
        """Given simple straight words, compute standard word score."""
        super().compute_word_score(squares, tilebag)


class WordExtension(BaseWord):
    """Represent an extended word."""

    def __init__(self, word, **kwargs):
        self.word = word
        self.parent = kwargs.get("parent", None)
        self.front_part = kwargs.get("front", None)
        self.back_part = kwargs.get("back", None)
        self.front_part_xy = None
        self.back_part_xy = None

    def compute_word_score(self, squares, tilebag):
        """Given a word extension, compute turn score."""
        super().compute_word_score(squares, tilebag)

    @property
    def coord(self):
        if not self.front_part_xy:
            return self.parent.coord
        return self.front_part_xy


class WordCrosses(BaseWord):
    """Represent an extended word."""

    def __init__(self, word, **kwargs):
        self.word = word
        self.parent = kwargs.get("parent", None)
        self.front_part = kwargs.get("front", None)
        self.back_part = kwargs.get("back", None)
        self.front_part_xy = None
        self.back_part_xy = None
        self.direction = None
        self.coord = (None, None)
        self.score = None

    def compute_word_score(self, squares, tilebag):
        """Given a word extension, compute turn score."""
        super().compute_word_score(squares, tilebag)


class BonusWord(BaseWord):
    """Represent an additional word created by playing another."""

    def __init__(self, word, **kwargs):
        super().__init__(word, **kwargs)

    def compute_word_score(self, tilebag):
        """Bonus words only count letter scores."""
        self.score = sum([tilebag[letter].value for letter in self.word])


class PlayedWords(object):
    """Represent all played words."""

    def __init__(self, **kwargs):
        """Establish a list of played words."""
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

    @property
    def word_list(self):
        """Return list of word strings"""
        return [x.word for x in self]
