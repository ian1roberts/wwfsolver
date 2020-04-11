"""Compute word crosses."""
from wwfs.config import DICT


def get_valid_word_crosses(word, job_data):
    """Compute all possible word overlaps. Mainly rack words."""
    word_crosses = []
    candidates = get_word_crosses(word, DICT, job_data.rack)
    if candidates:
        for candidate in candidates:
            is_valid, bonus_words = is_valid_move(
                                        job_data.board, word,
                                        candidate, job_data.tilebag)
            if is_valid:
                tot_score = is_valid.score + sum(
                                        [x.score for x in bonus_words])
                word_crosses.append({"type": "crosses", "data":
                                    (word, is_valid, bonus_words,
                                     tot_score)})
    # print("Word Crosses for {} done. {} found.".format(
    #                                     word, len(job_data.word_crosses)))
    job_data.queue.put(word_crosses)


def get_word_crosses(word, DICT, rack):
    """Get all valid words that cross existing board words."""
    pass


def is_valid_move(board, word, candidate, tilebag):
    """Check that candidate word is a legal move played on word."""
