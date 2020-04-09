from wwfs.config import DICT


class Turn(object):
    """Calculate best legal word move in game."""

    def __init__(self, rack, played_words, board, debug=False):
        """Construct the board for analysis."""
        self.rack = rack
        self.all_played = played_words
        self.board = board
        if not debug:
            self.word_extensions = self.get_valid_word_extensions()
            self.word_crosses = self.get_valid_word_crosses()
            self.word_runs = self.get_valid_word_runs()
            self.best_word()

    def get_valid_word_extensions(self):
        """Compute all possible word extensions."""
        # get all extensions of played words
        playable = dict(zip([x for x in self.all_played],
                            [set() for _ in self.all_played]))
        for word in self.all_played:
            candidates = word.get_word_extensions(DICT, self.rack)
            if candidates:
                for candidate in candidates:
                    is_valid, bwords = self.board.is_valid_move_extends(
                                                               word, candidate)
                    if is_valid:
                        playable[word].add(candidate)
                    if len(bwords) > 0:
                        [playable[word].add(x) for x in bwords]
        return playable

    def get_valid_word_crosses(self):
        """Compute all possible word overlaps. Mainly rack words."""

    def get_valid_word_runs(self):
        """Compute all possible word run along."""

    def best_word(self):
        """Compute_best move."""
        #  return word
