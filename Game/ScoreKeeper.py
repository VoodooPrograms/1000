

class ScoreKeeper:

    def __init__(self, players):
        self.score_table = {}
        self.winner = None
        for player in players:
            self.score_table[player.name] = 0

    def is_game_finished(self):
        for player, player_score in self.score_table.items():
            if player_score > 1000:
                self.winner = player
                return True
        return False

    def update_score_table(self, scores: dict):
        print(scores)
        for player, score in scores.items():
            self.score_table[player] += score
        return self.is_game_finished()

