import pytest
import wwfs.wwfs as wwfs


class Args(object):
    """Dummy arguments class for testing argument parsing."""
    load = None
    save = "wwfsolver_game_data.pkl"
    board = None
    tilebag = None
    status = None
    mode = None
    rack = None
    coord = None
    direction = None
    next_play = None
    player = None
    _debug = True


def test_args_p1new():
    "Parse command line arguments: player1 new game."
    my_args = Args()
    my_args.load = False
    my_args.player1 = True
    my_args.rack = "thecatw"
