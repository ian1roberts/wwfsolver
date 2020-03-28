"""Application wrapper for wwfs."""
import argparse
from wwfs.wwfs import main

parser = argparse.ArgumentParser(description=("Words With Friends Puzzle"
                                              "Solver"))
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-p', '--player1',
                   help="Player 1 turn",
                   action="store_true")
group.add_argument('-o', '--player2',
                   help="Player 2 turn",
                   action="store_true")
group.add_argument('-c', '--coord',
                   help="XY coordinate of first tile_letter",
                   action="store_true")
group.add_argument('-d', '--direction',
                   help="Direction of word", type=str)

parser.add_argument('-s', '--save',
                    help='Save the active board.',
                    default='wwfs.tsv', type=str)
parser.add_argument('-l', '--load',
                    help='Load in game board.',
                    default='wwfs.tsv', type=str)

# main positional argument is the filename of a template board
parser.add_argument('board', help='filename of board')
parser.add_argument('tilebag', help="filename of tilebag")
parser.add_argument('rack', help='letters in rack, use 0 for blanks')

parser.add_argument('-v', '--version', action='version',
                    version='%(prog)s 0.1')


def run_wwfs():
    """Launch application via this main routine."""
    args = parser.parse_args()
    main(args)
