from typing import List
import unittest
from datetime import datetime

from lol_updater import locator
from lol_updater import iterfactory

from . import utils


API_KEY = 'f561197a-82ea-4e54-acd2-386979018a7a'


class TestLocator(unittest.TestCase):

    def load_test_links(self) -> List[locator.Link]:
        return [
            locator.Link.from_dict(d) for d in utils.load_items('match_data_links.json')
        ]

    def test_link_serializer(self):
        link_data = utils.load_items('match_data_links.json')

        for d in link_data:
            link = locator.Link.from_dict(d)
            self.assertEqual(link.name, d['name'])
            self.assertEqual(link.ts, locator.parse_dt(d['updatedAt']))

    def test_latest_link(self):
        links = sorted(self.load_test_links(), reverse=True)
        # descending order
        for i in range(1, len(links)):
            self.assertLess(links[i].ts, links[i-1].ts)

    def test_download_latest(self):
        current_latest = datetime(2022, 6, 4, 3, 34, 53)
        latest_link = self.load_test_links()[0]
        ngames = 0
        nplayergames = 0
        nteamgames = 0
        if latest_link.ts > current_latest:
            for game in iterfactory.csv_game_iterator(current_latest, locator.download_games(latest_link.link)):
                ngames += 1
                nplayergames += len(game.playergames)
                nteamgames += len(game.teamgames)
        print('Games: {}, Player games: {}, Team games: {}'.format(
            ngames,
            nplayergames,
            nteamgames
        ))
        self.assertGreater(ngames, 0)

    # def test_link_downloader(self):
    #     links = locator.get_links(API_KEY)
    #     self.assertGreater(len(links), 0)


if __name__ == '__main__':
    # run the actual unittests
    unittest.main()
