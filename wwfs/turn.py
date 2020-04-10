from wwfs.config import DICT
import wwfs.extends as extends
import wwfs.crosses as crosses
import wwfs.runalongs as runs


class Turn(object):
    """Calculate best legal word move in game."""

    def __init__(self, rack, played_words, board, debug=False):
        """Construct the board for analysis."""
        self.rack = rack
        self.all_played = played_words
        self.board = board
        if not debug:
            self.get_valid_word_extensions()
            self.word_crosses = self.get_valid_word_crosses()
            self.word_runs = self.get_valid_word_runs()
            self.best_word()

    def get_valid_word_extensions(self):
        """Compute all possible word extensions."""
        # get all extensions of played words
        self.word_extensions = []
        for word in self.all_played:
            candidates = extends.get_word_extensions(word, DICT, self.rack)
            if candidates:
                for candidate in candidates:
                    is_valid, bonus_words = extends.is_valid_move_extention(
                                                self.board, word, candidate)
                    if is_valid:
                        self.word_extensions.append((is_valid, bonus_words))

    def get_valid_word_crosses(self):
        """Compute all possible word overlaps. Mainly rack words."""

    def get_valid_word_runs(self):
        """Compute all possible word run along."""

    def best_word(self):
        """Compute_best move."""
        playable = set()
        # collect all candidates
        for word, bonus in self.word_extensions:
            print(word, bonus)
        #  return word
