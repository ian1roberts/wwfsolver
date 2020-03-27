"""Board builds a playing grid from input code."""

import pandas as pd
key = {"sl": "single letter", "dl": "double letter", "tl": "triple letter",
       "dw": "double word", "tw": "triple word", "c": "center"
       }


class Square(object):
    """Represents an individual square on the word board.
       Squares hold letter tiles."""

    def __init__(self, x, y, tilemultiplier):
        """Represent a Square on the board, given a tile code multiplier."""
        self.x = x
        self.y = y
        self.tile_multiplier = tilemultiplier
        self.tile_multiplier_name = key[tilemultiplier]
        self.tile_letter = None
        self.player = None
        self.parent_word = None
        self.free = True

    def __str__(self):
        """x:0    y:0 v:single letter letter."""
        return "x:{}\ty:{}\tv:{}\t{}".format(self.x, self.y,
                                             self.tile, self.letter)


class Board(object):
    """Represents a board of tiles."""

    def __init__(self, layout=None):
        """Represent the whole board, given a filename to parse."""
        self._index = {}
        self.grid = None
        self.tile_grid = None
        self.width = len(self.grid.columns) if self.grid else None
        self.height = len(self.grid.index) if self.grid else None
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
            msg += ' {:^2}({:>2}, {:>2})'.format(i.tile_multiplier, i.x, i.y)
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