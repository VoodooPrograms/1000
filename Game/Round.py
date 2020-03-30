

class Round:

    CONTRACTS = (c for c in range(100, 210, 10))

    def __init__(self, players):
        self.players = players
        self.score_table = {player.name: 0 for player in self.players}
        self.current_player = list(self.score_table.keys())[0]
        self.card_stack = []
        self.pot = 100
        self.contract = None

    def set_contract(self, suit):
        self.contract = suit

    def next_player(self):
        self.current_player += 1

    def set_pot(self, pot):
        self.pot = pot

    def get_highest_card(self):
        pass