"""This file contains code for testing the nginx logfile reader

Running:
- `python3 -m tests.test_parsers`

or you can run in vscode like this: export PYTHONPATH=`pwd`; code .
"""

import datetime
import unittest

from lol_updater import parsers

from . import utils

# map input column names to game attributes if different
GAME_KEYMAP = dict(
    status='datacompleteness',
    duration='gamelength'
)


class TestGame(unittest.TestCase):

    def test_player_game(self):
        game_data = utils.get_player_game()
        game = parsers.Game.from_row(game_data)
        for key, value in game.as_dict().items():
            if key not in ('playergames', 'teamgames'):
                self.assertEqual(
                    value,
                    game_data[GAME_KEYMAP.get(key, key)]
                )

    def test_make_game_id(self):
        now = datetime.datetime.now()
        league = 'LCS'
        game = 1
        gameid = parsers.make_game_id(league, now, game)
        self.assertTrue(gameid.startswith(league))
        self.assertTrue(gameid.endswith(str(game)))
        self.assertTrue(now.strftime(parsers.GAME_ID_FORMAT) in gameid)

    def test_parse_bool(self):
        for v in (1, 2, True, 'true', '1', 'yes', 'Yes', 'True'):
            self.assertTrue(parsers.parse_bool(v))
        for v in (None, '', 0, '0', False, 'no', 'false'):
            self.assertFalse(parsers.parse_bool(v))


if __name__ == '__main__':
    # run the actual unittests
    unittest.main()
