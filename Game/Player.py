

class Player:

    def __init__(self, name, color=None, human=False):
        self.name = name
        self.color = color
        self.human = human
        self.hand = []
        # TornadoWS attributes eg. url, ws

    def __str__(self):
        return f'Player {self.name}'

    def set_card_in_hand(self, card):
        self.hand.append(card)

    def get_card_from_hand(self, card):
        return self.hand.pop(card)
