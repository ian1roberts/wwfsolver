"""Track the game play turn by turn."""


class Status(object):
    """Keep a current log of game play. Provide scoring report."""

    def __init__(self, gd):
        """Construct a new status object for a new game."""
        self.current_board = gd['board']
        self.current_tilebag = gd['tilebag']
        self.current_word = None
        self.current_player = gd['player']
        self.word_grid_loc_start = gd['coord']
        self.word_direction = gd['direction']
        self.turn_count = 0
        self.player1_history = []
        self.player2_history = []

    def update_log(self):
        """End of turn update logs."""
        pass


class Turn(object):
    """Represent a player's turn. Compute state change of board."""

    def __init__(self):
        """Construct the turn order of events. Compute the post turn outcome."""
        pass


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
            best_first_word = self.rack.compute_best_word(self.board,
                                                          self.tilebag)



    def player2_turn(self):
        """Player 2 takes a turn."""


    def record_turn(self):
        """Tidy up end of turn, log scores and words."""
        pass

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
