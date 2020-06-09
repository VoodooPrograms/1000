

class Player:

    def __init__(self, name, color=None, human=False):
        self.name = name
        self.color = color
        self.human = human
        self.hand = []
        # TornadoWS attributes eg. url, ws

    def __str__(self):
        return f'Player {self.name}'

    def setCardInHand(self, card):
        self.hand.append(card)

    def getCardFromHand(self, card):
        return self.hand.pop(card)

    def getHand(self):
        return self.hand

    def isHuman(self):
        pass

