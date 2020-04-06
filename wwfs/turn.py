"""Compute the next move."""
import itertools
from functools import reduce
from collections import Counter
from wwfs.utils import permute_rack, load_dictionary, is_valid_word

ALPHA = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
DICT = load_dictionary()


class Turn(object):
    """Calculate best legal word move in game."""

    def __init__(self, game_data, all_played_words):
        """Construct the board for analysis."""
        self.game_data = game_data
        self.all_played_words = all_played_words

    def get_valid_word_extensions(self):
        """Compute all possible word extensions."""
        # get all extensions of played words
        word_keys = set([x[0] for x in self.all_played_words])
        playable = set()

        for key in word_keys:
            keylen = len(key)
            key_letters = Counter([l for l in key])
            matches = [s for s in DICT if key in s and len(s) > keylen]
            # check that letter differences exist in rack
            for word in matches:
                word_letters = Counter([l for l in word])
                letter_diff = word_letters - key_letters
                if self.game_data["rack"].has_enough_letters(letter_diff,
                                                             word):
                    playable.add(word)
        return playable

    def get_valid_word_crosses(self):
        """Compute all possible word overlaps. Mainly rack words."""

    def get_valid_side_runs(self):
        """Compute all possible word run along."""

    def check_valid_move(self):
        """Is the board still valid given the move."""
