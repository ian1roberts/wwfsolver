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

    if args.player1:
        rack = Rack(args.rack)
        coord = None
        direction = None

    if args.player2:
        rack = args.rack
        coord = args.coord
        direction = args.direction

    if args.load:
        last_turn = utils.restore(args.load)
        board = last_turn['board']
        tilebag = last_turn['tilebag']
        status = last_turn['status']
        mode = "continue"

    game_data = dict(zip(['board', 'tilebag', 'status', 'rack', 'coord',
                          'direction', 'mode'],
                         [board, tilebag, status, rack, coord,
                         direction, mode]))
    game = Game(game_data)

    game.take_turn()
    game.record_turn()

    # Output results
    utils.print_board(game.turn)
    utils.print_best_word(game.best_word)

    utils.save(args.save, game)
