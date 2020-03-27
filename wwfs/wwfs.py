"""wwfs main routine.

"""
import wwfs.utils as utils
from wwfs.board import Board
from wwfs.words import Rack
from wwfs.tiles import TileBag


def opponent_turn(rack, grid, tilebag):
    """Play the opponents turn, update the grid and tilebag."""
    pass


def player_turn(rack, grid, tilebag):
    """Compute best hand to play from my rack, update grid and tilebag."""
    pass


def main(args):
    """Execute wwfs."""
    # Build the playing board for a new game
    if args.new:
        grid = Board(args.board)
        tilebag = TileBag(args.tilebag)
    else:
        # restore an active game
        grid, tilebag = utils.restore(args.load)

    # Build the rack
    rack = Rack(args.rack)

    # Opponent plays
    if args.opponent:
        turn = opponent_turn(rack, grid, tilebag)
    else:
        turn = player_turn(rack, grid, tilebag)

    # Output results
    utils.print_board(turn)
    utils.print_best_word(turn)

    utils.save(args.save, turn)
