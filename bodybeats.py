__all__ = ["PLAYER1", "PLAYER2", "bodybeats"]

PLAYER1, PLAYER2 = "drums", "piano"


class bodybeats:
    """
    A bodybeats game.
    """

    def __init__(self):
        self.moves = ''
        self.instrument = None
        self.winner = None

    def play(self, player, move):
        """
        Play moves.

        Returns the move string.

        """

        self.moves = move

        return move
