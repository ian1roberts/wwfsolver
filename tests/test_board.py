import pytest
from os import path as p
from pandas import DataFrame
from wwfs.board import Board, Square
from wwfs.word import Word


_wwfs = p.dirname(p.abspath(__file__))
test_data = p.join(_wwfs, '..', 'wwfs', 'data')


@pytest.fixture
def myboard():
    layout = p.join(test_data, 'board.csv')
    board = Board(layout)
    return board


def test_board_instansiate(myboard):
    """Can instansiate square object."""

    assert isinstance(myboard.grid, DataFrame)
    assert isinstance(myboard.tile_grid, DataFrame)


@pytest.mark.parametrize("word, x, y, direction, expected", [
    (Word("CAT"), 1, 1, 0, [Square(1, 1, 'dw'), Square(1, 2, 'sl'),
                            Square(1, 3, 'sl')]),
    (Word("CAT"), 1, 1, 1, [Square(1, 1, 'dw'), Square(2, 1, 'sl'),
                            Square(3, 1, 'sl')]),
    (Word("CAT"), 1, 8, 0, [Square(1, 8, 'sl'), Square(1, 9, 'dw'),
                            Square(1, 10, 'sl')]),
    (Word("CAT"), 1, 9, 0, False),
    (Word("CAT"), 8, 1, 1, [Square(8, 1, 'sl'), Square(9, 1, 'dw'),
                            Square(10, 1, 'sl')]),
    (Word("CAT"), 9, 1, 1, False)
])
def test_get_n_squares_from_xy_d(myboard, word, x, y, direction, expected):
    """Can retrieve a set of board squares given word coordinates."""
    squares = myboard.get_square_xy(word, x, y, direction)
    assert squares == expected


@pytest.mark.parametrize("word, expected", [
    (Word("CAT", coord=(1, 1), direction=0), [("C", 1, 1, True),
                                              ("A", 1, 2, True),
                                              ("T", 1, 3, True)]),
    (Word("FROG", coord=(2, 0), direction=1), [("F", 2, 0, True),
                                               ("R", 3, 0, True),
                                               ("O", 4, 0, True),
                                               ("G", 5, 0, True)])
])
def test_play_word(myboard, word, expected):
    """Can play word, test upating main Square attributes."""
    for i, (l, x, y, _r) in enumerate(expected):
        b = myboard.get_square_xy(Word(l), x, y, 0)[0]
        assert b.tile_letter == ""
        assert b.free
        assert b.x == x
        assert b.y == y
        assert b.parent_word == []
    myboard.play_word(word)
    for i, (l, x, y, r) in enumerate(expected):
        assert word.squares[i].tile_letter == l
        assert word.squares[i].tile_used == r
        assert not word.squares[i].free
        assert word.squares[i].parent_word == [word]
        assert word.squares[i].x == x
        assert word.squares[i].y == y


@pytest.mark.parametrize("target, ori, test_yes", [
    (Square(5, 5, "sl"), 'left', True),
    (Square(5, 5, "sl"), 'left', False),
    (Square(5, 5, "sl"), 'right', True),
    (Square(5, 5, "sl"), 'right', False),
    (Square(5, 5, "sl"), 'up', True),
    (Square(5, 5, "sl"), 'up', False),
    (Square(5, 5, "sl"), 'down', True),
    (Square(5, 5, "sl"), 'down', False),
])
def test_collides(myboard, target, ori, test_yes):
    """Test adjacent Square for possible collision."""
    #  test_yes = True when adjacent square is occupied (word collides)
    adjx, adjy = {'left': (target.x, target.y - 1),
                  'right': (target.x, target.y + 1),
                  'up': (target.x - 1, target.y),
                  'down': (target.x + 1, target.y)}[ori]
    adjsq = myboard.get_square_xy(Word('X'), adjx, adjy, 0)[0]
    if test_yes:
        adjsq.free = False
        test_yes = adjsq
    observed = myboard.collides(target, ori)
    assert observed == test_yes


@pytest.mark.parametrize("target, direction, ending, expected", [
    (Square(5, 5, "sl"), 0, 'front', True),
    (Square(5, 5, "sl"), 0, 'back', False),
    (Square(5, 5, "sl"), 1, 'front', True),
    (Square(5, 5, "sl"), 1, 'back', False)
])
def test_check_collision(myboard, target, direction, ending, expected):
    """Test that we can detect colliding words."""
    # TODO: Test only checks collisions on extended words. Generalize.
    # This is a wrapper to collides function.
    # Test by making all adjacent squares occupied if collision expected
    for ori in ['left', 'right', 'up', 'down']:
        adjx, adjy = {'left': (target.x, target.y - 1),
                      'right': (target.x, target.y + 1),
                      'up': (target.x - 1, target.y),
                      'down': (target.x + 1, target.y)}[ori]
        adjsq = myboard.get_square_xy(Word('X'), adjx, adjy, 0)[0]
        adjsq.free = not expected
    len_expected = 0 if not expected else 3
    observed = myboard.check_collisions(target, direction, ending)
    assert len(observed) == len_expected


def test_board_width(myboard):
    assert myboard.width == 11


def test_board_height(myboard):
    assert myboard.height == 11

# TODO: is_valid_move_extends (after Word)
