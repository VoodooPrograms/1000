import os


class Card:
    STATIC_FILENAME = "/static/images/"
    STATIC_FILENAME_EXT = ".png"

    def __init__(self, filename, rank, suit, value):
        self.filename = os.path.join(Card.STATIC_FILENAME, f'{filename}{Card.STATIC_FILENAME_EXT}')
        self.rank = rank
        self.suit = suit
        self.value = value

    """
    This will display html tags
    """
    def display(self):
        return self.filename

    def __str__(self):
        return f'{self.rank}{self.suit}'
