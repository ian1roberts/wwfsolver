"""wwfs main routine."""
import wwfs.utils as utils
from wwfs.board import Board
from wwfs.rack import Rack
from wwfs.tiles import TileBag
from wwfs.game import Game


def main(args):
    """ Main execution function for wwfs application.

    Parse command line arguments, instantiate Game object with parameters.
    Plays the turn, prints output and saves game state for next round.

    Arguments are read from a pickled save file if `load` filename is empty.

    Arguments
    ---------
    load : filename of saved game. Empty strings signifies new game.
    save : filename to save game state after turn. Default wwfs_game_data.pkl
    board : filename of comma separated values board design.
    tilebag : filename of comman separated values tile letter bag.
    rack : character string of up to 7 letter tiles for play.
    player1 : signifies its your turn.
    player2 : signifies its opponent's turn.
    coord : coordinates on board first letter (row, column) for player2 turn.
    direction : specify player2 turn 0=horiztonal play, 1=vertical play.

    Returns
    -------
    wwfs_game_data.pkl in invoked directory.
    """
    # Test for debug execution
    if hasattr(args, '_debug'):
        xgame = "DEBUG: "
    else:
        args._debug = False
        xgame = ""
    # Build the playing board for a new game - new if no supplied load filename
    if not args.load and args.player1:
        xgame += "Player 1 starts a new game."
    if not args.load and args.player2:
        xgame += "Player 2 starts a new game."
        raise NotImplementedError("Player2 starts new game is unsupported.")
    if args.load and args.player1:
        xgame += "Player 1 continues a game."
    if args.load and args.player2:
        xgame += "Player 2 continues a game."

    print(xgame)

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

    # Game is the main app object, invoke take_turn to play.
    game = Game(board=board, tilebag=tilebag, status=status, rack=rack,
                coord=coord, direction=direction, mode=mode, player=player)
    if not args._debug:
        game.take_turn()

    # Output results, and exit saving game state.
    print(game.print_board())
    print(game.print_status())
    utils.save(args.save, game)
    utils.dump_output(game, next_play)

    return xgame
