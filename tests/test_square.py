import pytest
from os import path as p
from wwfs.board import Square
from wwfs.word import Word

from wwfs.utils import load_dictionary

DICT = load_dictionary()

_wwfs = p.dirname(p.abspath(__file__))
test_data = p.join(_wwfs, '..', 'wwfs', 'data')


@pytest.mark.parametrize("x, y, tile_multiplier, tm_name, is_center", [
    (0, 0, "tw", "triple word", False),
    (1, 1, "dl", "double letter", False),
    (5, 5, "c", "center", True)
])
def test_square_instansiate(x, y, tile_multiplier, tm_name, is_center):
    """Can instansiate square object."""
    sq = Square(x, y, tile_multiplier)
    assert sq.tile_multiplier_name == tm_name
    assert sq.is_center_square == is_center


@pytest.mark.parametrize("ori, cword, direction, expected", [
    ("left", "T", 0, set(["BAT", ])),
    ("left", "D", 0, set(["BAD", ])),
    ("left", "X", 0, False)
])
def test_sq_collision_left_horiz_true(ori, cword, direction, expected):
    "Test valid word collison on square's left reading across."
    sq = Square(1, 1, "tw")
    sq.parent_word = [Word('BA', direction=0), ]
    assert sq.collision(ori, cword, direction, DICT) == expected


@pytest.mark.parametrize("ori, cword, direction, expected", [
    ("right", "T", 0, set(["TAP", ])),
    ("right", "G", 0, set(["GAP", ])),
    ("right", "Q", 0, False)
])
def test_sq_collision_right_horiz_true(ori, cword, direction, expected):
    "Test valid word collison on square's right reading across."
    sq = Square(1, 1, "tw")
    sq.parent_word = [Word('AP', direction=0), ]
    assert sq.collision(ori, cword, direction, DICT) == expected


@pytest.mark.parametrize("ori, cword, direction, expected", [
    ("up", "T", 1, set(["HAT", ])),
    ("up", "G", 1, set(["HAG", ])),
    ("up", "Z", 1, False)
])
def test_sq_collision_up_vert_true(ori, cword, direction, expected):
    "Test valid word collison on square's right reading across."
    sq = Square(1, 1, "tw")
    sq.parent_word = [Word('HA', direction=1), ]
    assert sq.collision(ori, cword, direction, DICT) == expected


@pytest.mark.parametrize("ori, cword, direction, expected", [
    ("down", "B", 1, set(["BAD", ])),
    ("down", "H", 1, set(["HAD", ])),
    ("down", "Z", 1, False)
])
def test_sq_collision_down_vert_true(ori, cword, direction, expected):
    "Test valid word collison on square's right reading across."
    sq = Square(1, 1, "tw")
    sq.parent_word = [Word('AD', direction=1), ]
    assert sq.collision(ori, cword, direction, DICT) == expected
