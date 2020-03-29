"""Track the game play turn by turn."""

import itertools


class Status(object):
    """Keep a current log of game play. Provide scoring report."""

    HEADER = ["Turn", "Player", "Total", "Word", "Score", "Coord", "Direction"]

    def __init__(self, gd):
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

    def __str__(self):
        """Log entry print out."""
        "Turn:{:>3}\t"

    def log_entry(self, player, total, gd):
        """Prepare log entry from game data."""
        d = {0: "Across", 1: "Down"}
        return dict(zip(self.HEADER,
                        [self.turn_count, player, total + gd['score'],
                         gd['word'], gd['score'], gd['xy'],
                         d[gd['direction']]]))

    def update(self, gd, player):
        """End of turn update logs."""
        self.turn_count += 1

        if player == 1:
            play = 'Player1'
            total = self.player1total
            self.player1_history.append(self.log_entry(play, total, gd))
        else:
            play = 'Opponent'
            total = self.player2total
            self.player2_history.append(self.log_entry(play, total, gd))

    @property
    def player1total(self):
        """Compute running total score for player 1."""
        return sum([x['Score'] for x in self.player1_history])

    @property
    def player2total(self):
        """Compute running total score for Opponent."""
        return sum([x['Score'] for x in self.player2_history])

# class Turn(object):
#     """Represent a player's turn. Compute state change of board."""
#
#     def __init__(self):
#         """Construct the turn order of events.Compute the post turn outcome."""
#         pass


class Game(object):
    """Track turn by turn moves of the game. Provide current state of game."""

    def __init__(self, game_data):
        """Set up a round of word play."""
        self.game_data = game_data

        if game_data['mode'] == 'new':
            self.game_data['status'] = Status(game_data)

    def take_turn(self):
        """Make the turn. Compute best word and play it."""
        if self.game_data['player'] == 1:
            self.player1_turn()
        else:
            self.player2_turn()

    def player1_turn(self):
        """Player 1 takes a turn."""
        # TODO: Player 1 new game; first turn. Places best rack word on board.
        # Selects highest scoring position.
        if self.game_data['mode'] == 'new':
            # Best first word
            self.rack.compute_word_scores(self.board, self.tilebag)
            self.rack.first_word(self.board)
            word = self.rack.best_first_word
            w, wl, score, x, y, d = word

            # Play the word
            squares = self.board.play_word(w, wl, x, y, d, 1)

            # Update status logs
            turn_data = {'word': w, 'score': score, 'xy': (x, y),
                         'direction': d, 'squares': squares}
            self.status.update(turn_data, player=1)
            self.tilebag.update(turn_data)

    def player2_turn(self):
        """Player 2 takes a turn."""
        w = self.game_data['rack'].opponent_word
        wl = len(w)
        x, y = self.game_data['coord']
        d = self.game_data['direction']
        squares = self.board.get_square_xy(x, y, wl, d)
        score = self.rack.compute_word_score(w, squares, self.tilebag)
        self.board.play_word(w, wl, x, y, d, 2)
        # Update status logs
        turn_data = {'word': w, 'score': score, 'xy': (x, y),
                     'direction': d, 'squares': squares}
        self.status.update(turn_data, player=2)
        self.tilebag.update(turn_data)

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
                m1 = "{:>3}\t {:<8}\t {:>4}\t {:<10}\t {:>4}\t {:^}\t {:^9}".format(
                                    *[str(x1[x]) for x in self.status.HEADER])
            if x2 and x2['Player']:
                m2 = "{:>3}\t {:<8}\t {:>4}\t {:<10}\t {:>4}\t {:^}\t {:^9}".format(
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

    @property
    def rack(self):
        """Accessor returns rack object."""
        return self.game_data['rack']

    @property
    def board(self):
        """Accessor returns board object."""
        return self.game_data['board']

    @property
    def tilebag(self):
        """Accessor returns tilebag object."""
        return self.game_data['tilebag']

    @property
    def status(self):
        """Accessor returns Status object."""
        return self.game_data['status']
