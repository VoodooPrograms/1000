

class Round:

    CONTRACTS = tuple(contract for contract in range(100, 210, 10))

    def __init__(self, players, current_player=0):
        self.players = players
        self.score_table = {player.name: 0 for player in self.players}
        self.current_player = current_player
        self.musik_current_player = 0
        self.playing_current_player = 0
        self.card_stack = []
        self.pot = 100
        self.last_pot = 90
        self.card_table = {}
        self.round_points = {key: 0 for key in range(4)}
        self.card_color = None
        self.musik = None
        self.contract = None
        self.leader_player = None
        self.passed_players = []

    def set_contract(self, suit):
        self.contract = suit

    def next_player(self):
        self.current_player = (self.current_player + 1) % 4

    def next_musik_player(self):
        self.musik_current_player += 1
        if self.musik_current_player == self.current_player:
            self.musik_current_player += 1

    def next_playing_player(self):
        self.playing_current_player = (self.playing_current_player + 1) % 4

    def get_contracts(self):
        print(f'Hej {self.pot} {self.current_player}')
        return (pot for pot in self.CONTRACTS if pot > self.last_pot)

    def set_pot(self, pot):
        if pot == "pass":
            self.passed_players.append(self.current_player)
            is_pot_finished = self.is_pot_finished()
            if is_pot_finished:
                self.next_player()
                while self.current_player in self.passed_players:
                    self.next_player()
        else:
            self.pot = int(pot)
            self.last_pot = int(self.pot)
            self.leader_player = self.current_player

        print(f'Licytacja {self.current_player}')
        is_pot_finished = self.is_pot_finished()
        if is_pot_finished:
            print(f'Licytacje wygrał {self.current_player}')
            return is_pot_finished
        else:
            self.next_player()
            while self.current_player in self.passed_players:
                self.next_player()

    def is_pot_finished(self):
        if self.pot == self.CONTRACTS[-1] or len(self.passed_players) == 3:
            print("Odkrycie musika, wysłanie jaki jest pot, zaczyna ten kto not in passed_players")
            return True
        else:
            return False

    def set_musik(self, musik):
        self.musik = musik

    def add_to_card_table(self, card):
        if len(self.card_table) == 0:
            self.card_color = card.suit
            self.check_for_marriage(self.players[self.playing_current_player], card)

        self.card_table[self.playing_current_player] = card
        if len(self.card_table) == 4:
            print("OCENIAMY")
            print(self.card_table)
            self.get_highest_card()
            self.card_color = None
            self.card_table = {}
            return True
        return False

    def get_highest_card(self):

        # sum values of all cards
        points = sum(card.value for card in self.card_table.values())

        # Only cards with suit of playing_player
        self.card_table = {player: card for player, card in self.card_table.items() if card.suit == self.card_color}

        # Get winner and highest card
        winner, highest_card = max(self.card_table.items(), key=lambda highest: highest[1].value)

        for card in self.card_table.values():
            print(f'{card.suit}{card.rank}{card.value}')

        self.add_round_points(winner, points)

        # Set winner as next player to play
        self.current_player = winner

    def check_for_marriage(self, player, placed_card):
        hand = player.hand
        print(hand)
        if placed_card.rank == 'Q' or placed_card.rank == 'K':
            for card in hand:
                if "K" == card.rank or "Q" == card.rank:
                    if placed_card.suit == card.suit:
                        print("Meldunek")
                        self.contract = card.suit
                        print(self.contract)
                        if placed_card.suit == "S":
                            points = 40
                        elif placed_card.suit == "C":
                            points = 60
                        elif placed_card.suit == "D":
                            points = 80
                        elif placed_card.suit == "H":
                            points = 100
                        self.add_round_points(self.playing_current_player, points)

    def add_round_points(self, winner, points):
        winner_name = self.players[winner].name
        print(f"Gracz {winner_name}{winner} dostał {points}")
        if winner in self.round_points.keys():
            self.round_points[winner] += points
            self.score_table[winner_name] += points

    def is_round_finished(self):
        if all([len(player.hand) == 0 for player in self.players]):
            print("KONIECCC")
            print("POINTS: ", self.round_points)
            print(self.pot)
            print(f'leader player:{self.leader_player}')
            if self.pot <= self.round_points[self.leader_player]:
                print("Ugrałeś")
                self.score_table[self.players[self.leader_player].name] = self.pot
            else:
                print("Nie ugrałeś")
                self.score_table[self.players[self.leader_player].name] = -self.pot
            return True
        return False
