"""Compute best scoring words."""
import itertools
from collections import Counter
from copy import copy
from wwfs.utils import permute_rack, is_valid_word
from wwfs.word import Word
from wwfs.config import DICT, ALPHA


class Rack(object):
    """Represents my rack of game letters.

    Game play logic.
    1. First turn --> first word can only be made from rack letters.
    2. Subsequent turns --> words must contain existing word letters.
        There are 3 possible move types:
            1. extend an existing word
            2. cross an existing word
            3. run along an existing word
        Word play may be a valid word with rack letters only or valid by
        incorporating existing played letters

        Word play may produce one or more valid words.
    """
    def __init__(self, letters, player=1):
        """Represent an active rack of tiles."""
        self.letters = list(letters.strip().upper())
        self.letters_no_blanks = [x for x in self.letters if x != '0']
        self.player = player
        self.racks = []
        if player == 1:
            # TODO: add played board letters to racks if accsesible to play
            self.make_racks()  # solve blanks
            self.compute_rack_words()

    @property
    def nblanks(self):
        """Return the number of blanks in rack."""
        return len(self.letters) - len(self.letters_no_blanks)

    def racks_from_blanks(self):
        """Add racks from solving blanks."""
        if self.nblanks == 2:
            x = itertools.product(ALPHA, repeat=2)
            d = set()
            for i in x:
                d.add("".join(sorted(list(i))))
                dd = list(d)
                dd.sort()
            for d in dd:
                rc = Counter(list(d) + self.letters_no_blanks)
                self.racks.append(rc)
            return

        for A in ALPHA:
            rc = Counter([A, ] + self.letters_no_blanks)
            self.racks.append(rc)

    def racks_from_played_word(self, word):
        """Extend racks from played word."""

    def make_racks(self):
        """Compute all playable racks by solving blanks."""
        # 1. Generate racks from blanks
        if self.nblanks:
            self.racks_from_blanks()

        # 2. Add in rack from nonblanks
        if not self.nblanks:
            self.racks.append(Counter(self.letters_no_blanks))

    def compute_rack_words(self, WordType=Word):
        """Permute rack letters to generate list of viable words."""
        self.words = set()
        for rack in self.racks:
            for word in permute_rack(list(rack.elements())):
                if is_valid_word(word, DICT):
                    # TODO: Handle extends, crosses and run alongs
                    self.words.add(WordType(word))  # Simple rack words only

    def compute_all_play_word_scores(self, board, tilebag):
        """Return the highest scoring word play for all rack words."""
        xword_scores = set()
        for word in self.words:
            for i, square in enumerate(board):
                for d in (0, 1):
                    squares = board.get_square_xy(word, square.x, square.y, d)
                    if squares:
                        xword = copy(word)
                        xword.compute_word_score(squares, tilebag)
                        xword.coord = square.coord
                        xword.direction = d
                        xword_scores.add(xword)

        self.word_scores = sorted(list(xword_scores), key=lambda x: (-x.score,
                                  x.word, x.x, x.y, x.direction))

    def first_word(self, board):
        """Return best word that passes through center square."""
        center = [i.coord for i in board if i.is_center_square][0]
        for word in self.word_scores:
            if word.coord == center:
                break
        self.best_first_word = word

    def has_enough_letters(self, ldiffs):
        """Return True if a rack has enough letters to play word."""
        for rack in self.racks:
            totdiff = sum(ldiffs.values())
            for l, c in ldiffs.items():
                if l in rack:
                    count = rack[l]
                    totdiff -= count
                    if count - c < 0:  # not enough letters, short circuit
                        break
            if totdiff < 1:
                return True
        return False

    @property
    def opponent_word(self):
        """Return player2's rack as a formatted word."""
        return "".join(self.letters_no_blanks)
