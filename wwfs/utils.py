"""A collection of useful Utility functions."""
import itertools
import pickle

WORDLIST = "/usr/share/dict/words"


def load_dictionary(wordlist=WORDLIST):
    """Return a list of known words parsed from WORDLIST."""
    words = set()
    with open(wordlist) as fhandle:
        for word in fhandle:
            if "'" in word or len(word) < 2:
                continue
            words.add(word.strip().upper())
    return words


def _chunks(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0
    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg
    return out


def permute_racks(racks, DICT):
    result = set()
    for rack in racks:
        maxlen = len(rack) + 1
        for wl in range(2, maxlen):
            for yword in itertools.permutations(rack, r=wl):
                yword = "".join(yword)
                if yword in DICT:
                    result.add(yword)
    return result


def is_valid_word(word, wordlist):
    """Check word is valid in the dictionary."""
    return True if word in wordlist else False


def save(fname, game_data):
    """Save game data at end of turn."""
    with open(fname, 'wb') as f:
        pickle.dump(game_data, f)


def load(fname):
    """Load game data at start of turn."""
    with open(fname, 'rb') as f:
        game_data = pickle.load(f)
        return game_data


def dump_output(game, next_play):
    """Wrap up turn by displaying status to screen."""
    print("Tiles remaining: {}\nNext play: {}.\n".format(
                                                    game.tilebag.remaining,
                                                    next_play))
    p1, p2 = game.status.player1total, game.status.player2total
    nturns = game.status.turn_count

    if game.tilebag.remaining < 1:
        outcome = game.status.report_winner()
        print("Game over. Player1: {}, Opponent: {}. Outcome: {}".format(
                                                            p1, p2, outcome))
    else:
        print("Player1: {}, Opponent: {}, Turns: {}".format(
                                                            p1, p2, nturns))
