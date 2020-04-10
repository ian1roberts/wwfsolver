"""Track the game play turn by turn."""

import itertools
from wwfs.turn import Turn
from wwfs.word import Word, PlayedWords


class Status(object):
    """Keep a current log of game play. Provide scoring report."""

    HEADER = ["Turn", "Player", "Total", "Word", "Score", "Coord", "Direction"]

    def __init__(self):
        """Construct a new status object for a new game."""
        self.turn_count = 0
        self.player1_history = [dict(zip(
                                         self.HEADER,
                                         [1000, False, False, False, 0,
                                          False, False]))]
        self.player2_history = [dict(zip(
                                         self.HEADER,
                                         [1000, False, False, False, 0, False,
                                          False]))]
        self.all_played = PlayedWords()

    def __str__(self):
        """Log entry print out."""
        "Turn:{:>3}\t"

    def log_entry(self, player, total, word):
        """Prepare log entry from game data."""
        d = {0: "Across", 1: "Down"}
        return dict(zip(self.HEADER,
                        [self.turn_count, player, total + word.score,
                         word.word, word.score, word.coord,
                         d[word.direction]]))

    def update(self, word):
        """End of turn update logs."""
        self.turn_count += 1
        self.all_played.add_word(word)

        if word.player == 1:
            play = 'Player1'
            total = self.player1total
            self.player1_history.append(self.log_entry(play, total, word))
        else:
            play = 'Opponent'
            total = self.player2total
            self.player2_history.append(self.log_entry(play, total, word))

    @property
    def player1total(self):
        """Compute running total score for player 1."""
        return sum([x['Score'] for x in self.player1_history])

    @property
    def player2total(self):
        """Compute running total score for Opponent."""
        return sum([x['Score'] for x in self.player2_history])


class Game(object):
    """Track turn by turn moves of the game. Provide current state of game."""

    def __init__(self, **kwargs):
        """Set up a round of word play."""
        self.board = kwargs.get('board', None)
        self.tilebag = kwargs.get('tilebag', None)
        self.status = kwargs.get('status', None)
        self.rack = kwargs.get('rack', None)
        self.coord = kwargs.get('coord', None)
        self.direction = kwargs.get('direction', None)
        self.player = kwargs.get('player', None)
        self.mode = kwargs.get('mode', None)

        if self.mode == 'new':
            self.status = Status()

    def take_turn(self):
        """Make the turn. Compute best word and play it."""
        if self.player == 1:
            word = self.player1_turn()
            word.player = 1
        else:
            word = self.player2_turn()
            word.player = 2
        word.played = True
        self.board.play_word(word)
        self.status.update(word)
        self.tilebag.update(word)

    def player1_turn(self):
        """Player 1 takes a turn."""
        # TODO: Player 1 new game; first turn. Places best rack word on board.
        # Selects highest scoring position.
        if self.mode == 'new':
            # Best first word --> Is only a simple straight word
            self.rack.compute_all_play_word_scores(self.board, self.tilebag)
            self.rack.first_word(self.board)
            word = self.rack.best_first_word
        else:
            # TODO: Player 1 continues game. Places best word on current board.
            # Computes highest scoring move across all exisitng viable moves.
            next_move = Turn(self.rack, self.status.all_played, self.board,
                             self.tilebag)
            # Extend existing word
            # Cross existing words
            # Run along exisiting words
            word = next_move.best_word()
        return word

    def player2_turn(self):
        """Player 2 takes a turn."""
        word = Word(self.rack.opponent_word)
        word.coord = self.coord
        word.direction = self.direction
        word.squares = self.board.get_square_xy(word, word.x, word.y,
                                                word.direction)
        word.compute_word_score(word.squares, self.tilebag)
        return word

    def print_board(self):
        """Quick dump of game board. Needs prettifying."""
        print(self.board)

    def print_status(self):
        """Produce running commentary on game."""
        msg = "{:>3}\t {:<8}\t {:>4}\t {:<10}\t {:^}\t {:^}\t {:^9}\n".format(
                                                        *self.status.HEADER)

        p1 = sorted(self.status.player1_history, key=lambda x: x['Turn'])
        p2 = sorted(self.status.player2_history, key=lambda x: x['Turn'])

        m1, m2 = "\nPlayer1 end of turns.", "\nOpponent end of turns."
        for x1, x2 in itertools.zip_longest(p1, p2):
            if x1 and x1['Player']:
                m1 = ("{:>3}\t {:<8}\t {:>4}\t {:<10}\t {:>4}\t {:^}\t"
                      "{:^9}").format(
                      *[str(x1[x]) for x in self.status.HEADER])
            if x2 and x2['Player']:
                m2 = ("{:>3}\t {:<8}\t {:>4}\t {:<10}\t {:>4}\t {:^}\t"
                      "{:^9}").format(
                      *[str(x2[x]) for x in self.status.HEADER])
        msg += "{}\n{}\n".format(m1, m2)
        return msg

    def report_winner(self):
        """Report current outcome."""
        p1 = self.status.player1total
        p2 = self.status.player2total

        if p1 == p2:
            outcome = 'Tie.'
        elif p1 > p2:
            outcome = "Player1."
        else:
            outcome = "Opponent."
        return outcome
