"""Compute best scoring words."""
import itertools
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
