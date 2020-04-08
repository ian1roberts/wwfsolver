import pytest
from os import path as p
import wwfs.wwfs as wwfs

_wwfs = p.dirname(p.abspath(__file__))
test_data = p.join(_wwfs, '..', 'wwfs', 'data')


class Args(object):
    """Dummy arguments class for testing argument parsing."""
    load = None
    save = p.join(_wwfs, 'data', "xwwfsolver_game_data.pkl")
    board = None
    tilebag = None
    status = None
    mode = None
    rack = None
    coord = None
    direction = None
    next_play = None
    player1 = None
    player2 = None
    version = 0.1
    _debug = True


def test_args_p1new():
    "Parse command line arguments: player1 new game."
    my_args = Args()
    my_args.load = False
    my_args.player1 = True
    my_args.rack = "thecatw"
    my_args.board = p.join(test_data, "board.csv")
    my_args.tilebag = p.join(test_data, "tiles.csv")

    expected = "DEBUG: Player 1 starts a new game."
    observed = wwfs.main(my_args)
    assert expected == observed


def test_args_p1continue():
    "Parse command line arguments: player1 continues game."
    my_args = Args()
    my_args.load = p.join(_wwfs, 'data', "wwfs_game_data_p1_turn1.pkl")
    my_args.player1 = True
    my_args.rack = "thecatw"
    my_args.board = p.join(test_data, "board.csv")
    my_args.tilebag = p.join(test_data, "tiles.csv")

    expected = "DEBUG: Player 1 continues a game."
    observed = wwfs.main(my_args)
    assert expected == observed


def test_args_p2new():
    "Parse command line arguments: player2 new game."
    my_args = Args()
    my_args.load = False
    my_args.player2 = True
    my_args.coord = "5, 5"
    my_args.direction = 1
    my_args.rack = "thecatw"
    my_args.board = p.join(test_data, "board.csv")
    my_args.tilebag = p.join(test_data, "tiles.csv")

    with pytest.raises(NotImplementedError):
        wwfs.main(my_args)


def test_args_p2continue():
    "Parse command line arguments: player2 continues game."
    my_args = Args()
    my_args.load = p.join(_wwfs, 'data', "wwfs_game_data_p1_turn1.pkl")
    my_args.player2 = True
    my_args.coord = "5, 5"
    my_args.direction = 1
    my_args.rack = "when"
    my_args.board = p.join(test_data, "board.csv")
    my_args.tilebag = p.join(test_data, "tiles.csv")

    expected = "DEBUG: Player 2 continues a game."
    observed = wwfs.main(my_args)
    assert expected == observed
