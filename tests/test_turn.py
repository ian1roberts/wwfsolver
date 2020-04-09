import pytest
from os import path as p
from wwfs.word import Word, PlayedWords
from wwfs.board import Board
from wwfs.rack import Rack
from wwfs.turn import Turn

_wwfs = p.dirname(p.abspath(__file__))
test_data = p.join(_wwfs, '..', 'wwfs', 'data')


@pytest.fixture
def myrack():
    return Rack("te0ro0y")


@pytest.fixture
def myword1():
    return Word("WATCH", coord=(5, 5), direction=0, score=52, player=1)


@pytest.fixture
def myword2():
    return Word("WHEN", coord=(5, 5), direction=1, score=20, player=2)


@pytest.fixture
def myall_played_words():
    p = PlayedWords()
    p.add_word(Word("WATCH", coord=(5, 5), direction=0, score=52, player=1))
    p.add_word(Word("WHEN", coord=(5, 5), direction=1, score=20, player=2))
    return p


@pytest.fixture
def myboard():
    return Board(p.join(test_data, 'board.csv'))


def test_turn_instansiate(myrack, myall_played_words, myboard):
    """Can instansiate Turn object."""
    myturn = Turn(myrack, myall_played_words, myboard, debug=True)
    assert isinstance(myturn, Turn)


def test_get_valid_word_extensions(myrack, myall_played_words, myboard,
                                   myword1, myword2):
    """Test can compute word extensions."""
    expected = {myword1: {'STOPWATCH', 'BAYWATCH', 'SWATCH'},
                myword2: {'WHENCE', 'WHENS'}}
    myturn = Turn(myrack, myall_played_words, myboard, debug=True)
    observed = myturn.get_valid_word_extensions()
    assert expected == observed
