# __all__ = ["PLAYER1", "PLAYER2", "bodybeats"]

# PLAYER1, PLAYER2 = "drums", "piano"


class bodybeats:
    """
    A bodybeats game.
    """

    def __init__(self):
        self.moves = ''

    def play(self, instrument, sound):
        """
        Play moves.

        Returns the sound string.

        """

        self.sound = sound

        return sound
