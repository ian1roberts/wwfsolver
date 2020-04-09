import pytest
from os import path as p
from wwfs.word import Word
from wwfs.board import Board, Square
from wwfs.tiles import TileBag
from wwfs.rack import Rack


_wwfs = p.dirname(p.abspath(__file__))
test_data = p.join(_wwfs, '..', 'wwfs', 'data')


@pytest.fixture
def myword():
    return Word("TASTY", coord=(5, 5), direction=0)


@pytest.fixture
def myboard():
    return Board(p.join(test_data, 'board.csv'))


@pytest.fixture
def mytilebag():
    return TileBag(p.join(test_data, 'tiles.csv'))


def test_word_instansiate(myword):
    """Can instansiate Word object."""
    assert isinstance(myword, Word)
    assert myword.word == "TASTY"
    assert myword.x == 5
    assert myword.y == 5
    assert len(myword) == 5


@pytest.mark.parametrize("word, squares, total", [
    (Word("CAT"), [Square(1, 1, 'dw'), Square(1, 2, 'sl'),
                   Square(1, 3, 'sl')], 12),
    (Word("FROG"), [Square(1, 1, 'dw'), Square(2, 1, 'sl'),
                    Square(3, 1, 'sl'), Square(4, 1, 'tl')], 30),
    (Word("HORSE"), [Square(5, 5, 'sl'), Square(5, 6, 'dw'),
                     Square(5, 7, 'sl'), Square(5, 8, 'sl'),
                     Square(5, 9, 'tw')], 42),
])
def test_compute_word_score(word, squares, mytilebag, total):
    """Test can compute word score."""
    word.compute_word_score(squares, mytilebag)
    assert word.score == total


@pytest.mark.parametrize("word, dictionary, rack, expected", [
    (Word("CAT"), set(["CATCH", "XXCAT", "XXXCATXXX"]), Rack("CH"),
        set(['CATCH'])),
    (Word("CAT"), set(["CATCH", "XXCAT", "XXXCATXXX"]), Rack("XX"),
        set(['XXCAT'])),
    (Word("CAT"), set(["CATCH", "XXCAT", "XXXCATXXX"]), Rack("XXXXXX"),
        set(['XXCAT', 'XXXCATXXX'])),
    (Word("CAT"), set(["CATCH", "XXCAT", "XXXCATXXX"]), Rack("CHXX"),
        set(["CATCH", "XXCAT"])),
    (Word("CAT"), set(["CATCH", "XXCAT", "XXXCATXXX"]), Rack("ABC"),
        set([])),
    (Word("CAT"), set(["CATCH", "XXCAT", "XXXCATXXX"]), Rack("CX0"),
        set(["CATCH", "XXCAT"])),
    (Word("CAT"), set(["CATCH", "XXCAT", "XXXCATXXX"]), None,
        set(["CATCH", "XXCAT", "XXXCATXXX"]))
])
def test_get_word_extensions(word, dictionary, rack, expected):
    """Test can find nested words."""
    observed = word.get_word_extensions(dictionary, rack)
    assert observed == expected


@pytest.mark.parametrize("word, candidate, expected", [
    (Word("CAT"), "CATCH", (False, "CH")),
    (Word("CAT"), "XXCAT", ('XX', False)),
    (Word("CAT"), "XXCATCH", ('XX', 'CH')),
    (Word("CAT"), "XXXCATXXX", ("XXX", "XXX")),
    (Word("CAT"), "BAZINGA", (False, False)),
    ])
def test_get_letter_overhangs(word, candidate, expected):
    """Test can compute front and back letter overhangs."""
    observed = word.get_letter_overhangs(candidate)
    assert observed == expected
