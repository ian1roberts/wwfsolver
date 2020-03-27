"""A collection of useful Utility functions."""
import itertools

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
