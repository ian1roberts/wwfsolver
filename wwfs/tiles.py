"""Represent tiles in WWFs and the tile bag."""
import pandas as pd

TILES = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0")


class Tile(object):
    """A collection of single letters."""

    def __init__(self, letter, total, value):
        """Instantiate a letter Title object with values."""
        self.letter = letter
        self.value = value
        self.total = total
        self.played = 0

    def __str__(self):
        """Print representation of a Tile object."""
        return("{} value:{} total:{} played:{} remaining:{}".format(
               self.letter, self.value, self.total, self.played, self.remaining
               ))

    @property
    def remaining(self):
        """Return the number of available letter tiles of the letter."""
        return self.total - self.played


class TileBag(object):
    """A collection of all the letter tiles available for play."""

    def __init__(self, fname):
        """Load the Tile Bag of letters at the start of a game."""
        self.tile_bag = self.initialise_bag(fname)
        self.played = []

    def __str__(self):
        """Print representation of a TileBag."""
        return "Bag has {} tiles remaining.".format(self.remaining)

    def __getitem__(self, index):
        """Slice a TileBag using a Letter code."""
        return self.bag[index]

    def __iter__(self):
        """Iterate over TileBag letters, return the Tile object."""
        for i in TILES:
            yield self.bag[i]

    def initialise_bag(self, fname):
        """Parse the tile bag recipe, and return the playable letters."""
        bag = {}
        _bag = pd.read_csv(fname)

        for _x, row in _bag.iterrows():
            letter, total, value = row
            letter = "0" if letter == "Space" else letter
            bag[letter] = Tile(letter, int(total), int(value))

        self.bag = bag

    def tiles_in_word(self, word):
        """Return tiles that make up word."""
        return [self[x] for x in word]

    def update(self, tiles):
        """Remove played letter tiles from bag."""
        used = self.tiles_in_word(tiles['word'])
        squares = tiles['squares']

        for tile, square in zip(used, squares):
            if square.tile_used:
                self.played.append(tile.letter)
                tile.played += 1

    @property
    def remaining(self):
        """Report the total number of tiles remaining in the bag."""
        return sum([x.remaining for x in self])
