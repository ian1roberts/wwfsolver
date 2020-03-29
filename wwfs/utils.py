"""A collection of useful Utility functions."""
import itertools
import pickle

WORDLIST = "/usr/share/dict/words"


def load_dictionary(wordlist=WORDLIST):
    """Return a list of known words parsed from WORDLIST."""
    words = set()
    with open(wordlist) as fhandle:
        for word in fhandle:
            words.add(word.strip().upper())
    return words


def permute_rack(rack):
    """Construct all 2 - 7 letter combinations from rack."""
    maxlen = len(rack) + 1
    for wl in range(2, maxlen):
        for i in itertools.permutations(rack, r=wl):
            yield("".join(i))


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
