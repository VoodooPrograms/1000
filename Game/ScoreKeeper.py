

class ScoreKeeper:

    def __init__(self, players):
        self.score_table = dict()
        for player in players:
            self.score_table[player.name] = 0

    def is_game_finished(self):
        for player_score in self.score_table:
            if player_score > 1000:
                return True
        return False

    def update_score_table(self, scores: dict):
        for player, score in scores:
            self.score_table[player.name] += score

    def get_scores(self):
        return self.score_table
