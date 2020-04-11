"""Computes the best next move."""

import multiprocessing as mp
from wwfs.extends import get_valid_word_extensions
from wwfs.crosses import get_valid_word_crosses
from wwfs.runalongs import get_valid_word_runs


class TurnData(object):
    """Delivers job data to parallel processes."""
    def __init__(self, **kwargs):
        self.word = kwargs.get("word", None)
        self.rack = kwargs.get("rack", None)
        self.board = kwargs.get('board', None)
        self.tilebag = kwargs.get('tilebag', None)
        self.word_extensions = []
        self.word_crosses = []
        self.word_runs = []


def do_task(xfunc, word, turn_data):
    """Wrapper function to multiprocessing."""
    return xfunc(word, turn_data)


class Turn(object):
    """Calculate best legal word move in game."""

    def __init__(self, rack, played_words, board, tilebag, debug=False):
        """Construct the board for analysis."""
        self.turn_data = TurnData(rack=rack, board=board, tilebag=tilebag)
        self.played_words = played_words
        self.turn_word = None
        self.turn_bonus_words = None
        self.turn_score = None
        self.proc_ids = []
        if not debug:
            self.compute_move()
            # self.best_word()

    def compute_move(self):
        """Parallel process next move."""
        processes = []
        pool = mp.Pool(4)
        mp_manager = mp.Manager()
        self.turn_data.queue = mp_manager.Queue(len(self.played_words) * 3)
        for word in self.played_words:
            for task in [get_valid_word_extensions,
                         get_valid_word_crosses, get_valid_word_runs]:
                processes.append(pool.apply_async(do_task,
                                 (task, word, self.turn_data, )))
        for xproc in processes:
            xproc.get()
        while not self.turn_data.queue.empty():
            self.proc_ids.append(self.turn_data.queue.get())

    def best_word(self):
        """Compute_best move."""
        self.playable = (self.turn_data.word_extensions +
                         self.turn_data.word_crosses +
                         self.turn_data.word_runs)
        sorted(self.playable, key=lambda x: x[2], reverse=True)
        self.turn_word = self.playable[0][0]
        self.turn_bonus_words = self.playable[0][1]
        self.turn_score = self.playable[0][2]
