import pytest
from os import path as p
from wwfs.board import Board
from wwfs.word import Word
from wwfs.tiles import TileBag


_wwfs = p.dirname(p.abspath(__file__))
test_data = p.join(_wwfs, '..', 'wwfs', 'data')


@pytest.fixture
def mytilebag():
    return TileBag(p.join(test_data, 'tiles.csv'))


@pytest.fixture
def myword():
    word = Word("TASTY", coord=(5, 5), direction=0)
    layout = p.join(test_data, 'board.csv')
    board = Board(layout)
    word.squares = board.get_square_xy(word, word.x, word.y, word.direction)
    for sq in word.squares:
        sq.tile_used = True
    return word


def test_tilebag_instansiate(mytilebag):
    """Can instansiate Word object."""
    assert isinstance(mytilebag, TileBag)
    assert mytilebag.remaining == 104
    assert mytilebag.played == []


def test_update(myword, mytilebag):
    """Remove tiles from tilebag aftern playing word."""
    mytilebag.update(myword)
    assert mytilebag.played == list('TASTY')
    assert mytilebag.remaining == (104 - len(myword))
