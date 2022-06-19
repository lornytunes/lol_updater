import datetime
from typing import List, Dict
from dataclasses import dataclass, field

import requests

MATCH_DATA_URL = 'https://oe.datalisk.io/matchData'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0'
DT_FORMAT = '%Y-%m-%dT%H:%M:%S.000Z'


def parse_dt(value: str) -> datetime:
    return datetime.datetime.strptime(value, DT_FORMAT)


def get_headers(api_key: str) -> Dict:
    return {
        'User-Agent': USER_AGENT,
        'Accept': 'application/json; indent=4',
        'X-Api-Key': api_key,
    }


@dataclass(order=True)
class Link:
    name: str
    link: str
    year: int
    games: int
    ts: datetime = field(init=True, compare=True)

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            data['name'],
            data['link'],
            int(data['year']),
            int(data['games']),
            parse_dt(data['updatedAt'])
        )

    @property
    def filename(self) -> str:
        return f"{self.ts.strftime('%Y%m%d')}.csv"


def get_links(api_key: str) -> List[Link]:
    req = requests.get(MATCH_DATA_URL, headers=get_headers(api_key))
    if req.status_code == 200:
        return [Link.from_dict(d) for d in req.json()]
    return []


def latest_link(links: List[Link]) -> Link:
    year = datetime.date.today().year
    current = [link for link in links if link.year == year]
    if current:
        return current[0]
    return None


def download_games(url: str) -> List[str]:
    req = requests.get(url)
    if req.status_code == 200:
        return req.text.splitlines()
    return []
