import unittest
from unittest.mock import Mock

from Game.ScoreKeeper import ScoreKeeper


class TestScoreKeeper(unittest.TestCase):

    def setUp(self):
        self.players = []
        names = ["Bartosz", "Adrianna", "Natalia", "Florencja"]
        for name in names:
            player_mock = Mock()
            player_mock.name = name
            self.players.append(player_mock)
        self.score_keeper = ScoreKeeper(self.players)

    def test_init(self):
        self.assertIsInstance(ScoreKeeper(self.players), ScoreKeeper)

    def test_is_game_finished(self):
        # Not winning edge case
        self.score_keeper.score_table = {player.name: 0 for player in self.players}
        self.assertFalse(self.score_keeper.is_game_finished())

        # Winning edge case
        self.score_keeper.score_table["Adrianna"] = 1000
        self.assertTrue(self.score_keeper.is_game_finished())

    def test_update_score_table(self):
        self.score_keeper.update_score_table({player.name: 30 for player in self.players})
        self.assertEqual(self.score_keeper.score_table["Natalia"], 30)
        self.assertDictEqual(self.score_keeper.score_table, {player.name: 30 for player in self.players})

        # Winning edge case
        self.score_keeper.score_table["Florencja"] = 990
        winning = self.score_keeper.update_score_table({player.name: 30 for player in self.players})
        self.assertTrue(winning)



