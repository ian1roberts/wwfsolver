"""wwfs main routine."""
import wwfs.utils as utils
from wwfs.board import Board
from wwfs.words import Rack
from wwfs.tiles import TileBag
from wwfs.turn import Game


def main(args):
    """Execute wwfs."""
    # Build the playing board for a new game
    # (assume new if no supplied load filename)
    if not args.load:
        board = Board(args.board)
        tilebag = TileBag(args.tilebag)
        status = None
        mode = "new"
    else:
        last_turn = utils.load(args.load)
        board = last_turn.board
        tilebag = last_turn.tilebag
        status = last_turn.status
        mode = "continue"

    if args.player1:
        rack = Rack(args.rack)
        coord = None
        direction = None
        player = 1
        next_play = "Opponent."

    if args.player2:
        rack = Rack(args.rack, player=2)
        coord = tuple(map(int, args.coord.split(",")))
        direction = args.direction
        player = 2
        next_play = "Player1."
    # Compile all essential information required to play the game.
    # Game is the main hub object, invokes take_turn the main method call.
    game = Game(board=board, tilebag=tilebag, status=status, rack=rack,
                coord=coord, direction=direction, mode=mode, player=player)
    game.take_turn()

    # Output results, and exit saving game state.
    print(game.print_board())
    print(game.print_status())
    utils.save(args.save, game)
    utils.dump_output(game, next_play)
