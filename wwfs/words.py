"""Compute best scoring words."""
import itertools
from functools import reduce
from wwfs.utils import permute_rack, load_dictionary, is_valid_word

ALPHA = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
DICT = load_dictionary()


class Rack(object):
    """Represents my rack of game letters."""

    def __init__(self, letters):
        """Represent an active rack of tiles."""
        self.letters = list(letters.strip().upper())
        self.letters_no_blanks = [x for x in self.letters if x != '0']
        self.racks = self.make_racks()
        self.words = set()
        self.compute_rack_words()
        self._dict = DICT

    def make_racks(self):
        """Return all playable racks by solving blanks."""
        # TODO: can use to add in played board letters
        racks = []

        # Handle blanks
        n_blanks = sum([1 for x in self.letters if x == '0'])

        if n_blanks == 1:
            for a in ALPHA:
                racks.append([a, ] + self.letters_no_blanks)
        elif n_blanks == 2:
            x = itertools.permutations(ALPHA, r=2)
            for i in x:
                racks.append(list(i) + self.letters_no_blanks)
        else:
            racks.append(self.letters_no_blanks)

        return racks

    def compute_rack_words(self):
        """Permute rack letters to generate list of viable words."""
        for rack in self.racks:
            for word in permute_rack(rack):
                if is_valid_word(word, DICT):
                    self.words.add(word)

    def compute_word_score(self, word, squares, tilebag):
        """Given word and tile squares, compute the word score."""
        assert len(word) == len(squares), "Word doesn't fit error."
        # convert letters to values
        letter_values = [tilebag[letter].value for letter in word]
        pair = zip(letter_values, squares)
        ls = []
        wms = []
        wm = 1
        for lv, m in pair:
            if m.tile_multiplier_name == 'triple word':
                wms.append(3)
            elif (m.tile_multiplier_name == 'double word' or
                  m.tile_multiplier_name == 'center'):
                wms.append(2)
            elif m.tile_multiplier_name == 'single letter':
                ls.append(lv)
            elif m.tile_multiplier_name == 'double letter':
                ls.append(lv * 2)
            elif m.tile_multiplier_name == 'triple letter':
                ls.append(lv * 3)
        ls = sum(ls)
        if len(wms) > 0:
            wm = reduce((lambda x, y: x * y), wms)
        return (ls * wm)

    def compute_word_scores(self, board, tilebag, best=False):
        """Return the highest scoring word play for all rack words."""
        scores = []
        for word in self.words:
            wlen = len(word)
            for i, square in enumerate(board):
                for d in (0, 1):
                    squares = board.get_square_xy(square.x, square.y, wlen, d)
                    if squares:
                        score = self.compute_word_score(word, squares, tilebag)
                        scores.append((word, wlen, score,
                                       square.x, square.y, d))

        self.word_scores = sorted(scores, key=lambda x: (-x[2], x[1], x[3],
                                                         x[4], x[5]))

    def first_word(self, board):
        """Return best word that passes through center square."""
        center = [(i.x, i.y) for i in board if i.is_center_square][0]
        for ws in self.word_scores:
            if (ws[3], ws[4]) == center:
                break
        self.best_first_word = ws
