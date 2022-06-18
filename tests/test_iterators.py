"""
This file contains code for testing custom csv iterators

Running:
- `python3 -m tests.test_iterators`

"""
import unittest
from datetime import datetime

from lol_updater import iterfactory

from . import utils


class TestLIterators(unittest.TestCase):

    def test_latest_iterator(self):
        # parse all rows newer than this
        latest = datetime(2022, 3, 1, 9, 0, 0)
        num_rows = 0
        with open(utils.get_games_file_csv('game_rows.csv'), 'r') as finput:
            for row in iterfactory.csv_latest_iterator(latest, finput):
                self.assertIsInstance(row, dict)
                num_rows += 1
        self.assertEqual(num_rows, 5)

    def test_game_iterator(self):
        latest = datetime(2022, 1, 14, 23, 5, 34)
        with open(utils.get_games_file_csv('games.csv'), 'r') as finput:
            games = [
                game for game in iterfactory.csv_game_iterator(latest, finput)
            ]
        for game in games:
            self.assertEqual(len(game.teamgames), 2)
        self.assertEqual(len(games), 3)
        output_file = utils.save_items(
            [game.as_dict() for game in games], 'games.json')
        print('Games saved to {}'.format(output_file))


if __name__ == '__main__':
    unittest.main()
