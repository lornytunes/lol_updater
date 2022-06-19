from typing import List, Dict
from pathlib import Path

import json
import csv

FIXTURES_DIR = Path(__file__).parent / 'fixtures'
OUTPUT_DIR = Path(__file__).parent / 'output'


def get_games(filename) -> List[Dict]:
    with open(Path(FIXTURES_DIR, filename), 'r') as fp:
        return json.load(fp)


def load_game(filename) -> Dict:
    with open(Path(FIXTURES_DIR, filename), 'r') as finput:
        reader = csv.DictReader(finput)
        row = next(reader)
    return row


def get_games_file_csv(filename) -> Path:
    return Path(FIXTURES_DIR, filename)


def load_player_game() -> Dict:
    return load_game('player_game.csv')


def load_team_game() -> Dict:
    return load_game('team_game.csv')


def get_player_game() -> Dict:
    return get_games('player_game.json')[0]


def get_team_game() -> Dict:
    return get_games('team_game.json')[0]


def save_item(item: Dict, filename: str) -> str:
    path = Path(OUTPUT_DIR, filename)
    with open(path, 'w') as foutput:
        json.dump(item, foutput, indent=4)
    return path.as_posix()


def save_items(items: List[Dict], filename: str) -> str:
    path = Path(OUTPUT_DIR, filename)
    with open(path, 'w') as foutput:
        json.dump(items, foutput, indent=4)
    return path.as_posix()


def load_item(filename: str) -> Dict:
    path = Path(FIXTURES_DIR, filename)
    with open(path, 'r') as finput:
        return json.load(finput)


def load_items(filename: str) -> List[Dict]:
    path = Path(FIXTURES_DIR, filename)
    with open(path, 'r') as finput:
        return json.load(finput)
