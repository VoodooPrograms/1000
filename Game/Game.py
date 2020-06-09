import json

from Game import Deck
from Game.Card import Card
from Game.JsonEncoder import JsonEncoder
from Game.MessageWriter import MessageWriter
from Game.Player import Player
from Game.Round import Round
from Game.ScoreKeeper import ScoreKeeper


class Game:
    def __init__(self, players):
        self.players = players
        self.deck = None
        self.current_player = -1
        self.state = "ON"
        self.score_table = None
        self.round = None
        self.init_score_table()
        self.init_round()

    def create_deck(self):
        self.deck = Deck.Deck()

    def init_hands(self):
        for player in self.players:
            self.deck.deal_card(player)

    def init_round(self):
        self.create_deck()
        self.init_hands()
        print(f'current player game {self.current_player}')
        self.next_player()
        self.round = Round(self.players, self.current_player)

    def init_score_table(self):
        self.score_table = ScoreKeeper(self.players)

    # from musik and from musik player to other players
    def give_cards(self, musik):
        for card in musik:
            self.players[self.round.current_player].setCardInHand(Card(card["filename"].split('/').pop()[:-4], card["rank"], card["suit"], card["value"]))

    def transfer_card(self, player1, player2, card):
        p1 = self.players[player1]
        p2 = self.players[player2]
        p2.setCardInHand(p1.getCardFromHand(card))

    def next_player(self):
        self.current_player = (self.current_player + 1) % 4

    def set_user(self):
        pass

    def deal_cards(self):
        pass

    def bid_ask(self):
        pass

    def make_move(self):
        pass

    def set_username(self, message):
        pass

    def update_chat(self, message):
        pass

    def add_player(self, player):
        self.players.add(Player(player))


"""
Serwer jest ON
    - Czeka na połączenie 4 graczy
    - Jak połączy się 4 graczy to włącza instancje gry Game.Game()
Game
    - Ustawia początkowe zasady(ustawia pierwszego i drugiego gracza)
    - Włącza Round.Round()
    Round
        - Tasowanie talii
        - Rozdanie kart
        - Ustawienie musika
        - Zaczęcie licytacji
        Licytacja
            - Pierwszy gracz jest ustawiony jako licytujący, drugi gracz podejmuje decyzje(UI do wyboru puli 100, 110 eg.)
            - Gracz może spassować z licytacji
            - Licytacja trwa dopóki nie zostanie ostatni gracz. Jest on wybierany na ugranie
            - Wyświetlenie musika
            - Rozdanie kart innym graczom
        - Round.Turn() rozpoczyna turę
        Round.Turn
            - Gracz pierwszy rzuca kartę, kolejni robią to samo
            - Podczas rzucania jest sprawdzane czy gracz ma meldunek
            - Funkcja oceniająca kto wygrywa karty
        - Round.Turn trwa dopóki gracze mają karty
        - Round.CountPoints() - sprawdza kto ile punktów zdobył i przyznaje je do puli
    - Game.Game() trwa dopóki któryś z graczy nie zdobędzie 1000 punktów
Server
    - W przypadku disconnectu, zawiesza grę i wyświetla komunikat


Komunikaty:
    - Connection/Disconnection
    - S - Wysłanie do gracza, że może wykonać ruch
    - C - Wykonuje ruch
"""