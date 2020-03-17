from Game import Hand


class Player():

    hand = Hand.Hand()

    def __init__(self, name, color=None, human=False):
        self.name = name
        self.color = color
        self.human = human

        # TornadoWS attributes eg. url, ws

    def __str__(self):
        return f'Player {self.name}'

    def setCardInHand(self, card):
        pass

    def getHand(self):
        pass

    def isHuman(self):
        pass
