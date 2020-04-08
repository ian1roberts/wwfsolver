"""Compute best scoring words."""
import itertools
from collections import Counter
from copy import copy
from wwfs.utils import permute_rack, load_dictionary, is_valid_word
from wwfs.word import Word

ALPHA = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
DICT = load_dictionary()


class Rack(object):
    """Represents my rack of game letters."""

    def __init__(self, letters, player=1):
        """Represent an active rack of tiles."""
        self.letters = list(letters.strip().upper())
        self.letters_no_blanks = [x for x in self.letters if x != '0']
        if player == 1:
            self.racks = self.make_racks()
            self.words = set()
            self.compute_rack_words()
        self._dict = DICT

    def make_racks(self):
        """Return all playable racks by solving blanks."""
        racks = []
        self.counter_racks = []

        # Handle blanks
        n_blanks = sum([1 for x in self.letters if x == '0'])

        if n_blanks == 2:
            x = itertools.product(ALPHA, repeat=2)
            d = set()
            for i in x:
                d.add("".join(sorted(list(i))))
                dd = list(d)
                dd.sort()
            for d in dd:
                racks.append(list(d) + self.letters_no_blanks)
                rc = Counter(list(d) + self.letters_no_blanks)
                self.counter_racks.append(rc)
        elif n_blanks == 1:
            for A in ALPHA:
                racks.append([A, ] + self.letters_no_blanks)
                rc = Counter([A, ] + self.letters_no_blanks)
                self.counter_racks.append(rc)
        else:
            racks.append(self.letters_no_blanks)
            self.counter_racks.append(Counter(self.letters_no_blanks))

        return racks

    def compute_rack_words(self):
        """Permute rack letters to generate list of viable words."""
        for rack in self.racks:
            for word in permute_rack(rack):
                if is_valid_word(word, DICT):
                    self.words.add(Word(word))

    def compute_word_scores(self, board, tilebag, best=False):
        """Return the highest scoring word play for all rack words."""
        scores = set()
        for word in self.words:
            for i, square in enumerate(board):
                for d in (0, 1):
                    squares = board.get_square_xy(word, square.x, square.y, d)
                    if squares:
                        xword = copy(word)
                        xword.compute_word_score(squares, tilebag)
                        xword.coord = square.coord
                        xword.direction = d
                        scores.add(xword)

        self.word_scores = sorted(list(scores), key=lambda x: (-x.score,
                                  x.word, x.x, x.y, x.direction))

    def first_word(self, board):
        """Return best word that passes through center square."""
        center = [i.coord for i in board if i.is_center_square][0]
        for word in self.word_scores:
            if word.coord == center:
                break
        self.best_first_word = word

    def has_enough_letters(self, ldiff, word):
        """Return True if a rack has enough letters to play word."""
        for rack in self.counter_racks:
            totdiff = sum(ldiff.values())
            for l, c in ldiff.items():
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
