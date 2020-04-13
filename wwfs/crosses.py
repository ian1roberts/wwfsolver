"""Compute word crosses."""
from wwfs.word import WordCrosses


def get_valid_word_crosses(word, job_data, debug=False):
    """Compute all possible word overlaps. Mainly rack words."""
    word_crosses = []
    job_data.rack.racks_from_played_word(word)
    job_data.rack.compute_rack_words(word, WordCrosses)

    for candidate in job_data.rack.words:
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
    if debug:
        return word_crosses
    job_data.queue.put(word_crosses)


def is_valid_move(board, word, candidate, tilebag):
    """Check that candidate word is a legal move played on word."""
