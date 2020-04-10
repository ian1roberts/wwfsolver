"""Board builds a playing grid from input code."""

import pandas as pd
from functools import total_ordering
from wwfs.config import DICT
from wwfs.word import BonusWord
# from wwfs.wwfsexception import CollisionError

key = {"sl": "single letter", "dl": "double letter", "tl": "triple letter",
       "dw": "double word", "tw": "triple word", "c": "center"
       }


@total_ordering
class Square(object):
    """Represents an individual square on the word board.

       Squares hold letter tiles.
    """

    def __init__(self, x, y, tilemultiplier):
        """Represent a Square on the board, given a tile code multiplier."""
        self.x = x
        self.y = y
        self.coord = (x, y)
        self.tile_multiplier = tilemultiplier
        self.tile_multiplier_name = key[tilemultiplier]
        self.tile_letter = ""
        self.player = -1
        self.parent_word = []
        self.free = True

    def __hash__(self):
        return hash((self.x, self.y, self.tile_multiplier_name))

    def __eq__(self, other):
        return (self.x, self.y, self.tile_multiplier_name) == (
                                  other.x, other.y, other.tile_multiplier_name)

    def __lt__(self, other):
        return self.index < other.index

    def __str__(self):
        """x:0    y:0 v:single letter letter."""
        return "x:{}\ty:{}\tv:{}\t{}".format(self.x, self.y,
                                             self.tile_multiplier_name,
                                             self.tile_letter)

    @property
    def is_center_square(self):
        """Return True if square is the center square."""
        return True if self.tile_multiplier_name == "center" else False

    def collision_word(self, ori, candidate, direction, side_letter,
                       DICT=DICT):
        """Return word collision if valid, else False."""
        collision_words = set()
        for parent_word in self.parent_word:
            crash_word = {
                            ("left", 0, 0): (parent_word.word, candidate),
                            ("left", 1, 0): (self.tile_letter, candidate),
                            ("left", 0, 1): (parent_word.word, side_letter),
                            ("left", 1, 1): (self.tile_letter, side_letter),
                            ("right", 0, 0): (candidate, parent_word.word),
                            ("right", 1, 0): (side_letter, parent_word.word),
                            ("right", 0, 1): (candidate, self.tile_letter),
                            ("right", 1, 1): (side_letter, self.tile_letter),
                            ("up", 0, 0): (self.tile_letter, side_letter),
                            ("up", 1, 0): (parent_word.word, side_letter),
                            ("up", 0, 1): (self.tile_letter, candidate),
                            ("up", 1, 1): (parent_word.word, candidate),
                            ("down", 0, 0): (side_letter, self.tile_letter),
                            ("down", 1, 0): (candidate, self.tile_letter),
                            ("down", 0, 1): (side_letter, parent_word.word),
                            ("down", 1, 1): (candidate, parent_word.word)
                        }[(ori, parent_word.direction, direction)]
            bword = "".join(crash_word)
            if bword not in DICT:
                return False
            a, b = crash_word
            if type(a) == str:
                coord = (self.coord)
                bd = direction
            else:
                coord = parent_word.coord
                bd = parent_word.direction
            bword = BonusWord(bword, coord=coord, direction=bd)
            print(bword)
            bword.left_part = a
            bword.right_part = b
            collision_words.add(bword)

        return collision_words


class Board(object):
    """Represents a board of tiles."""

    def __init__(self, layout=None):
        """Represent the whole board, given a filename to parse."""
        self._index = {}
        self.grid = None
        self.tile_grid = None
        if layout:
            self.load_board(layout)
            self.create_board()

    def __getitem__(self, index):
        """Slicing Board returns a tile square, given an integer index."""
        return self._index[index]

    def __str__(self):
        """Print the board in two letter code format."""
        msg = ""
        x = 0
        for i in self:
            if i.x > x:
                msg += '\n'
                x = i.x
            msg += ' {:^2}({:>2},{:>2}){:^1}'.format(
                            i.tile_multiplier, i.x, i.y, i.tile_letter)
        return msg

    def __iter__(self):
        """Iterate over tiles of the board, return tile."""
        i = 0
        while i < len(self._index):
            yield self[i]
            i += 1

    def load_board(self, layout):
        """Create a playing board from a layout filenmae."""
        self.grid = pd.read_csv(layout, header=None)

    def create_board(self):
        """Parse the layout to create a playable board."""
        self.tile_grid = pd.DataFrame(index=self.grid.index,
                                      columns=self.grid.columns)
        counter = 0
        for x, row in self.grid.iteritems():
            for y, xytile in row.iteritems():
                tile = Square(x, y, xytile)
                tile.index = counter
                self._index[counter] = tile
                self.tile_grid[x][y] = tile
                counter += 1

    def get_square_xy(self, word, x, y, d):
        """Return a set of squares if include wlen and direction."""
        ylim = y + len(word)
        xlim = x + len(word)
        if d == 0:
            if self.width >= ylim:
                return [self.tile_grid[x][i] for i in range(y, ylim)]
            return False
        if self.height >= xlim:
            return [self.tile_grid[i][y] for i in range(x, xlim)]
        return False

    def play_word(self, word):
        """Given a word and coordinates, position word on board."""
        word.squares = self.get_square_xy(word, word.x, word.y, word.direction)
        for letter, square in zip(word.word, word.squares):
            if square.free:
                square.free = False
                square.tile_letter = letter
                square.tile_used = True
            else:
                square.reused = True
                square.tile_used = False
            square.parent_word.append(word)

    def collides_on_side(self, square, ori):
        """Returns true if tested square collides with adjacent square ori."""
        x, y = square.coord
        if ori == 'up':
            x -= 1
        if ori == "down":
            x += 1
        if ori == "left":
            y -= 1
        if ori == "right":
            y += 1
        if y >= self.width or y < 0:
            return False
        if x >= self.height or x < 0:
            return False

        adjacent = self.tile_grid[x][y]
        if adjacent.free:
            return False
        return adjacent

    def check_collisions(self, square, direction, ending):
        """Check if playing a square would clash with a neighbour word.
        Returns the colliding squares, adjacent of the Target letter.
        [("up", adj.square), ... ]
        """
        collisions = []
        front_hori = ['up', 'down', 'left']  # addition to front, grow left
        back_hori = ['up', 'down', 'right']  # adddition to back, grow right
        front_vert = ['up', 'left', 'right']
        back_vert = ['down', 'left', 'right']
        oris = {('front', 0): front_hori, ('back', 0): back_hori,
                ('front', 1): front_vert, ('back', 1): back_vert}[
                                                        (ending, direction)]
        for ori in oris:
            check_square = self.collides_on_side(square, ori)
            if check_square:
                collisions.append((ori, check_square))
        return collisions

    @property
    def width(self):
        """Return number of columns on board."""
        return len(self.tile_grid.columns)

    @property
    def height(self):
        """Return the number of rows on the board."""
        return len(self.tile_grid.index)
