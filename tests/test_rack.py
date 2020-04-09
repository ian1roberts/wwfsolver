import pytest
from os import path as p
from collections import Counter
from wwfs.word import Word
from wwfs.board import Board
from wwfs.tiles import TileBag
from wwfs.rack import Rack


_wwfs = p.dirname(p.abspath(__file__))
test_data = p.join(_wwfs, '..', 'wwfs', 'data')


@pytest.fixture
def myrack():
    return Rack("ABCDEFG")


@pytest.fixture
def myword():
    return Word("TASTY", coord=(5, 5), direction=0)


@pytest.fixture
def myboard():
    return Board(p.join(test_data, 'board.csv'))


@pytest.fixture
def mytilebag():
    return TileBag(p.join(test_data, 'tiles.csv'))


def test_rack_instansiate(myrack):
    """Can instansiate Rack object."""
    assert isinstance(myrack, Rack)
    assert myrack.player == 1
    assert myrack.letters == ["A", "B", "C", "D", "E", "F", "G"]
    assert myrack.letters_no_blanks == ["A", "B", "C", "D", "E", "F", "G"]
    assert len(myrack.words) == 45


@pytest.mark.parametrize("hits, tot_scores, wlen, expected", [
    (45, 8778, 2, 220), (45, 8778, 3, 198), (45, 8778, 4, 176),
    (45, 8778, 5, 154)
])
def test_compute_all_play_word_scores(myrack, myboard, mytilebag,
                                      hits, tot_scores, wlen, expected):
    """Test can compute word score."""
    #  For a given word length wlen, there are expected number of board plays
    #  Each board play must have a score. Check that wlen expected number of
    #  scores are computed for each of hits words.  Hits words makes tot_scores
    #  plays = 2 x ((w - ((k -1)) x w) ... w = width of board, k = word length
    #  for square boards: 2 .. 220, 3 .. 198, 4 .. 176, 5 .. 154
    #  board = 11 x 11 (w x h)
    myrack.compute_all_play_word_scores(myboard, mytilebag)
    count = Counter()
    for i in myrack.word_scores:
        count[i.word] += 1
    xa = {len(x) for x in myrack.words}
    xb = {x for x in count.values()}
    observed = dict(zip(sorted(list(xa)), sorted(list(xb), reverse=True)))
    assert len(myrack.words) == hits
    assert len(myrack.word_scores) == tot_scores
    assert observed[wlen] == expected


def test_first_word(myrack, myboard, mytilebag):
    """Test first played is highest scoring word that passes through center."""
    myrack.compute_all_play_word_scores(myboard, mytilebag)
    myrack.first_word(myboard)
    assert (myrack.best_first_word.__hash__() ==
            Word('DECAF', coord=(5, 5), direction=0).__hash__())


@pytest.mark.parametrize("ldiffs, expected", [
    (Counter("XXX"), False), (Counter("ABCDEFG"), True),
    (Counter('AA'), False), (Counter('ADGG'), False)
])
def test_has_enough_letters(myrack, ldiffs, expected):
    """Test that rack contains enough letters to make a longer word,
    given a base word."""
    observed = myrack.has_enough_letters(ldiffs)
    assert expected == observed

# TODO: Test blanks in Rack
