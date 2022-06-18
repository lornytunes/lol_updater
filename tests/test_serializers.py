"""This file contains code for testing the lol updater serialization of data classes

Running:
- `python3 -m tests.test_serializers`

"""

import unittest

from lol_updater import parsers

from . import utils


class TestSerializers(unittest.TestCase):

    def test_player_game_serialization(self):
        game_data = utils.get_player_game()
        game = parsers.Game.from_row(game_data)
        output_file = utils.save_item(game.as_dict(), 'player_game.json')
        game2 = parsers.Game.from_dict(utils.load_item(output_file))
        self.assertEquals(game, game2)
        print('Player game saved to {}'.format(output_file))

    def test_team_game_serialization(self):
        game_data = utils.get_team_game()
        game = parsers.Game.from_row(game_data)
        output_file = utils.save_item(game.as_dict(), 'team_game.json')
        game2 = parsers.Game.from_dict(utils.load_item(output_file))
        self.assertEquals(game, game2)
        print('Team game saved to {}'.format(output_file))


if __name__ == '__main__':
    # run the actual unittests
    unittest.main()
