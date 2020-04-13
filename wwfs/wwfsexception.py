"""Custom exceptions in wwfs game play."""


class CollisionError(Exception):
    def __init__(self, word, msg=""):
        super().__init__()
        print("Playing {} at {} causes a collision.\n{}".format(
                                                word.word, word.coord, msg))
