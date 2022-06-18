"""This file contains code for testing data class loading from csv rows

Running:
- `python3 -m tests.test_loaders`

"""

import unittest

from lol_updater import parsers

from . import utils


class TestLoaders(unittest.TestCase):

    def test_player_game_serialization(self):
        game_row = utils.load_player_game()
        game = parsers.Game.from_row(game_row)
        output_file = utils.save_item(game.as_dict(), 'player_game_csv.json')
        # game2 = parsers.Game.from_dict(utils.load_item(output_file))
        # self.assertEquals(game, game2)
        print('Player game saved to {}'.format(output_file))

    def test_team_game_serialization(self):
        game_row = utils.load_team_game()
        game = parsers.Game.from_row(game_row)
        output_file = utils.save_item(game.as_dict(), 'team_game_csv.json')
        print('Team game saved to {}'.format(output_file))


if __name__ == '__main__':
    # run the actual unittests
    unittest.main()
