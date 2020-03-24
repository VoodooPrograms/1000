from random import shuffle

from Game import Card, Player


class Deck:
    SUITS = ["D", "H", "S", "C"]
    RANKS = ["9", "10", "J", "Q", "K", "A"]
    VALUES = [9, 10, 11, 12, 13, 14]

    def __init__(self):
        self.cards = []
        self.create_deck()

    def create_deck(self):
        for suit in self.SUITS:
            for i, rank in enumerate(self.RANKS):
                self.cards.append(Card.Card(f'{rank}{suit}', rank, suit, self.VALUES[i]))
        self.shuffle()

    def shuffle(self):
        shuffle(self.cards)

    def create_musik(self, size=4):
        musik = list()
        for i in range(size):
            musik.append(self.cards.pop())
        return musik

    def deal_card(self, player: Player, amount: int = 5):
        for i in range(amount):
            card_to_pass = self.cards.pop()
            player.setCardInHand(card_to_pass)

    def size(self):
        return len(self.cards)

    def dump(self):
        for card in self.cards:
            print(card.display())
