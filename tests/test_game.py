import pytest
from os import path as p
from wwfs.word import Word, PlayedWords
from wwfs.board import Board
from wwfs.tiles import TileBag
from wwfs.rack import Rack
from wwfs.game import Game, Status

_wwfs = p.dirname(p.abspath(__file__))
test_data = p.join(_wwfs, '..', 'wwfs', 'data')


@pytest.fixture
def myrack():
    return Rack("te0ro0y")


@pytest.fixture
def myword1():
    return Word("WATCH", coord=(5, 5), direction=0, score=52, player=1)


@pytest.fixture
def myword2():
    return Word("WHEN", coord=(5, 5), direction=1, score=20, player=2)


@pytest.fixture
def myall_played_words():
    p = PlayedWords()
    p.add_word(Word("WATCH", coord=(5, 5), direction=0, score=52, player=1))
    p.add_word(Word("WHEN", coord=(5, 5), direction=1, score=20, player=2))
    return p


@pytest.fixture
def myboard():
    return Board(p.join(test_data, 'board.csv'))


@pytest.fixture
def mystatus():
    return Status()


def mp_player_turn(self, word):
    """Game turns method is not tested here.
    Monkeypatch skips over game logic."""
    self.board = Board(p.join(test_data, 'board.csv'))
    word.squares = self.board.get_square_xy(word,
                                            word.x, word.y, word.direction)
    for sq in word.squares:
        sq.tile_used = True
    self.tilebag = TileBag(p.join(test_data, 'tiles.csv'))
    word.played = True
    self.status = Status()
    self.status.update(word)
    self.tilebag.update(word)


@pytest.fixture(autouse=True)
def MPGame(monkeypatch):
    monkeypatch.setattr("wwfs.game.Game.player1_turn", mp_player_turn)
    monkeypatch.setattr("wwfs.game.Game.player2_turn", mp_player_turn)


def test_status_instansiate():
    """Test can instansiate Status object."""
    assert isinstance(Status(), Status)


@pytest.mark.parametrize("player, total, expected", [
    ("Player1", 10, {"Turn": 0, "Player": "Player1", "Total": 62,
                     "Word": "WATCH", "Score": 52, "Coord": (5, 5),
                     "Direction": "Across"}),
    ("Opponent", 15, {"Turn": 0, "Player": "Opponent", "Total": 35,
                      "Word": "WHEN", "Score": 20, "Coord": (5, 5),
                      "Direction": "Down"})
])
def test_can_add_log_entry(mystatus, myword1, myword2, player, total,
                           expected):
    word = {"Player1": myword1, "Opponent": myword2}[player]
    observed = mystatus.log_entry(player, total, word)
    assert observed == expected


@pytest.mark.parametrize("player, expected", [
    (1, 52),
    (2, 20)
])
def test_status_update(mystatus, myword1, myword2, player, expected):
    word = {1: myword1, 2: myword2}[player]
    mystatus.update(word)
    (ptot, phist) = {1: ("player1total", "player1_history"),
                     2: ("player2total", "player2_history")}[player]
    assert expected == getattr(mystatus, ptot)
    assert len(getattr(mystatus, phist)) == 2


@pytest.mark.parametrize("word, expected", [
    (Word("WATCH", coord=(5, 5), direction=0, score=52, player=1), 52),
    (Word("WHEN", coord=(5, 5), direction=0, score=20, player=1), 20),
])
def test_take_turn(word, expected):
    """Test game take turn."""
    mygame = Game()  # monkeypatched
    mygame.player = word.player
    if word.player == 1:
        mygame.player1_turn(word)
        assert mygame.status.player1total == expected
    else:
        mygame.player2_turn(word)
        assert mygame.status.player2total == expected
