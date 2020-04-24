

class Round:

    CONTRACTS = (100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200)

    def __init__(self, players):
        self.players = players
        self.score_table = {player.name: 0 for player in self.players}
        self.current_player = 0 #list(self.score_table.keys())[0]
        self.card_stack = []
        self.pot = 100
        self.last_pot = 90
        self.musik = None
        self.contract = None
        self.passed_players = []

    def set_contract(self, suit):
        self.contract = suit

    def next_player(self):
        self.current_player += 1
        if self.current_player == len(self.players):
            self.current_player = 0

    def get_contracts(self):
        print(f'Hej {self.pot} {self.current_player}')
        return (pot for pot in self.CONTRACTS if pot > self.last_pot)

    def set_pot(self, pot):
        if pot == "pass":
            self.passed_players.append(self.current_player)
        else:
            self.pot = int(pot)
            self.last_pot = int(self.pot)

        self.next_player()
        while self.current_player in self.passed_players:
            self.next_player()

        return self.is_pot_finished()

    def is_pot_finished(self):
        if self.pot == 200 or len(self.passed_players) == 3:
            print("Odkrycie musika, wysłanie jaki jest pot, zaczyna ten kto not in passed_players")
            return True
        else:
            return False

    def set_musik(self, musik):
        self.musik = musik


    def get_highest_card(self):
        pass
