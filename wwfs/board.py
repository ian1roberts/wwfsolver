"""Board builds a playing grid from input code."""

import pandas as pd
from wwfs.word import Word
from wwfs.utils import load_dictionary

DICT = load_dictionary()

key = {"sl": "single letter", "dl": "double letter", "tl": "triple letter",
       "dw": "double word", "tw": "triple word", "c": "center"
       }


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

    def __str__(self):
        """x:0    y:0 v:single letter letter."""
        return "x:{}\ty:{}\tv:{}\t{}".format(self.x, self.y,
                                             self.tile_multiplier_name,
                                             self.tile_letter)

    @property
    def is_center_square(self):
        """Return True if square is the center square."""
        return True if self.tile_multiplier_name == "center" else False

    def collision(self, ori, candidate, direction, DICT=DICT):
        """Return word collision if valid, else False."""
        collision_words = set()
        print("Ori:{} Cand:{} Direct:{}".format(ori, candidate, direction))
        if ori == 'left' and direction == 0:
            for pword in self.parent_word:
                if pword.drection == 0:
                    cword = pword.word + candidate
                    if cword not in DICT:
                        return False
                    collision_words.add(cword)
        if ori == 'right' and direction == 0:
            for pword in self.parent_word:
                if pword.drection == 0:
                    cword = candidate + pword.word
                    if cword not in DICT:
                        return False
                    collision_words.add(cword)
        if ori == 'up' and direction == 1:
            for pword in self.parent_word:
                if pword.drection == 1:
                    cword = pword.word + candidate
                    if cword not in DICT:
                        return False
                    collision_words.add(cword)
        if ori == 'down' and direction == 1:
            for pword in self.parent_word:
                if pword.drection == 0:
                    cword = candidate + pword.word
                    if cword not in DICT:
                        return False
                    collision_words.add(cword)
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

    def is_valid_move_extends(self, word, candidate):
        """Candidate word can be legally played on top of word on board."""
        #  get letter / square overhangs
        need_front, need_back = word.get_letter_overhangs(candidate)
        #  test overhangs are playable
        bonus_words = []
        if need_front:
            if word.direction == 0:
                x = word.x
                y = word.y - len(need_front)
                if x < 0:
                    return (False, [])
            else:
                x = word.x - len(need_front)
                y = word.y
                if y < 0:
                    return (False, [])
            tmp_word = Word(need_front, coord=(x, y), direction=word.direction)
            front_squares = self.get_square_xy(tmp_word, x, y, word.direction)
            if front_squares is False:
                return (False, [])
            print(word)
            print(candidate)
            for i, j in zip(need_front, front_squares):
                if j.free:
                    # check neighbour Squares
                    print('Check Collisions: {}\tj{}'.format(i, j))
                    collisions = self.check_collisions(j, word.direction,
                                                       'front')
                    if collisions:
                        for (ori, collides) in collisions:
                            collision_word = collides.collision(ori,
                                                                candidate,
                                                                word.direction)
                            if not collision_word:
                                return (False, [])
                            else:
                                for bword in collision_word:
                                    bonus_words.append(bword)

                elif j.tile_letter == i:
                    continue
                else:
                    return (False, [])

        if need_back:
            if word.direction == 0:
                x = word.x
                y = word.y + len(word)
                if x >= self.width:
                    return (False, [])
            else:
                x = word.x + len(word)
                y = word.y
                if y >= self.height:
                    return (False, [])
            tmp_word = Word(need_back, coord=(x, y), direction=word.direction)
            back_squares = self.get_square_xy(tmp_word, x, y, word.direction)
            if back_squares is False:
                return (False, [])
            for i, j in zip(need_back, back_squares):
                if j.free:
                    # check neighbour Squares
                    collisions = self.check_collisions(j, word.direction,
                                                       'back')
                    if collisions:
                        for (ori, collides) in collisions:
                            collision_word = collides.collision(ori,
                                                                candidate,
                                                                word.direction)
                            if not collision_word:
                                return (False, [])
                            else:
                                for bword in collision_word:
                                    bonus_words.append(bword)
                elif j.tile_letter == i:
                    continue
                else:
                    return (False, [])

        # check whether extra words have been made
        if bonus_words:
            return (True, bonus_words)
        return (True, [])

    def collides(self, square, ori):
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
        """Check if playing a square would clash with a neighbour word."""
        collisions = []
        front_hori = ['up', 'down', 'left']
        back_hori = ['up', 'down', 'right']
        front_vert = ['up', 'left', 'right']
        back_vert = ['down', 'left', 'right']
        oris = {('front', 0): front_hori, ('back', 0): back_hori,
                ('front', 1): front_vert, ('back', 1): back_vert}[
                                                        (ending, direction)]
        for ori in oris:
            check_square = self.collides(square, ori)
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
