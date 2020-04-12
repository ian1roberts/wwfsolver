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


def do_task(xfunc, word, turn_data):
    """Wrapper function to multiprocessing."""
    return xfunc(word, turn_data)


class Turn(object):
    """Calculate best legal word move in game."""

    def __init__(self, rack, played_words, board, tilebag, debug=False):
        """Construct the board for analysis."""
        self.turn_data = TurnData(rack=rack, board=board, tilebag=tilebag)
        self.played_words = played_words
        self.anchor_word = None
        self.turn_word = None
        self.turn_bonus_words = None
        self.turn_score = None
        self.extensions = []
        self.crosses = []
        self.runs = []
        self.playable = []
        if not debug:
            self.compute_move()
            self.best_word()

    def __str__(self):
        return ("Play: {} at: {}:{} scores: {}. Bonus words: {}\n"
                "Considered: {} words out of Extensions: {}, Crosses: {}, Ru"
                "ns: {}.").format(
                self.turn_word.word, self.turn_word.coord,
                self.turn_word.direction, self.turn_score,
                " ".join([x.word for x in self.turn_bonus_words]),
                len(self.playable), len(self.extensions), len(self.crosses),
                len(self.runs)
                )

    def compute_move(self):
        """Parallel process next move."""
        processes = []
        mp_manager = mp.Manager()
        self.turn_data.queue = mp_manager.Queue(len(self.played_words) * 3)
        with mp.Pool(4) as pool:
            for word in self.played_words:
                for task in [get_valid_word_extensions,
                             get_valid_word_crosses, get_valid_word_runs]:
                    processes.append(pool.apply_async(do_task,
                                     (task, word, self.turn_data, )))
            for xproc in processes:
                xproc.get()
            pool.close()
            pool.join()
            result_types = {"extensions": self.extensions,
                            "crosses": self.crosses, "runs": self.runs}
            while not self.turn_data.queue.empty():
                results = self.turn_data.queue.get()
                if results:
                    for result in results:
                        result_type = result_types[result["type"]]
                        result_type.append(result['data'])

        self.playable = self.extensions + self.crosses + self.runs
        self.playable.sort(key=lambda x: x[3], reverse=True)

    def best_word(self):
        """Compute_best move."""
        self.anchor_word = self.playable[0][0]
        self.turn_word = self.playable[0][1]
        self.turn_bonus_words = self.playable[0][2]
        self.turn_score = self.playable[0][3]
