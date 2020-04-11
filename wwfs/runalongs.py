"""Compute word runalongs."""
import os
from wwfs.config import DICT


def get_valid_word_runs(word, job_data):
    """Compute all possible word run along."""
    job_data.queue.put(os.getpid())
    candidates = get_word_runs(word, DICT, job_data.rack)
    if candidates:
        for candidate in candidates:
            is_valid, bonus_words = is_valid_move(
                                        job_data.board, word,
                                        candidate, job_data.tilebag)
            if is_valid:
                tot_score = is_valid.score + sum(
                                        [x.score for x in bonus_words])
                job_data.word_runs.append((is_valid, bonus_words, tot_score))
    # print("Word Runalongs for {} done. {} found.".format(
    #                                     word, len(job_data.word_runs)))


def get_word_runs(word, DICT, rack):
    """Get all valid words that run along existing board words."""
    pass


def is_valid_move(board, word, candidate, tilebag):
    """Check that candidate word is a legal move played on board."""
    pass
