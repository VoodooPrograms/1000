
class Card:
    STATIC_FILENAME = "/static/images/"
    STATIC_FILENAME_EXT = ".png"

    def __init__(self, filename, rank, suit, value):
        self.filename = f'{Card.STATIC_FILENAME}{filename}{Card.STATIC_FILENAME_EXT}'
        self.rank = rank
        self.suit = suit
        self.value = value

    def getRank(self):
        return self.rank

    def getSuit(self):
        return self.suit

    def getValue(self):
        return self.value

    """
    This will display html tags
    """
    def display(self):
        return self.filename

    def __str__(self):
        return f'{self.rank}{self.suit}'
