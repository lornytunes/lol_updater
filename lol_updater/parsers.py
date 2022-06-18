from itertools import chain
from typing import Iterable, Dict, Any, List
from datetime import datetime
from collections import OrderedDict

from dataclasses import dataclass, field

INPUT_DT_FORMAT = '%Y-%m-%dT%H:%M:%S'
EA_DT_FORMAT = '%Y-%m-%d %H:%M:%S'
# if we need date times to generate a game id
GAME_ID_FORMAT = '%Y-%m-%d_%H-%M'


def slugify(value: str) -> str:
    return value.replace(' ', '-').lower()


def parse_dt(value: str) -> datetime:
    if value is None:
        return None
    for fmt in (INPUT_DT_FORMAT, EA_DT_FORMAT):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass
    return None


def parse_id(value: str) -> str:
    if value is None or value == '':
        return None
    if ':' not in value:
        return value
    return value.split(':')[-1]


def parse_bool(value: Any) -> bool:
    if value is None:
        return False
    elif isinstance(value, str):
        return value.lower() in ('1', 'true', 'yes')
    return bool(value)


def parse_int(value: str, default=0) -> int:
    if value:
        try:
            return int(value)
        except ValueError:
            pass
    return default


def parse_str(value: str, default=None) -> str:
    if value is None:
        return None
    value = value.strip()
    return value and value or default


def make_game_id(league: str, date: datetime, game: int) -> str:
    return f'{league}_{date.strftime(GAME_ID_FORMAT)}_{game}'


@dataclass
class Player:

    playerid: str
    name: str

    @classmethod
    def from_row(cls, row: Dict):
        playerid = parse_id(row['playerid'])
        name = parse_str(row['playername'], 'Unknown')
        if playerid is None:
            playerid = slugify(name)
        return cls(
            playerid,
            name
        )

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            data['playerid'],
            data['name']
        )

    def as_dict(self) -> OrderedDict:
        return OrderedDict(
            playerid=self.playerid,
            name=self.name
        )


@dataclass
class Team:

    teamid: str
    name: str

    @classmethod
    def from_row(cls, row: Dict):
        teamid = parse_id(row['teamid'])
        name = parse_str(row['teamname'], 'Unknown')
        if teamid is None:
            teamid = slugify(name)
        return cls(
            teamid,
            name
        )

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            data['teamid'],
            data['name']
        )

    def as_dict(self) -> OrderedDict:
        return OrderedDict(
            teamid=self.teamid,
            name=self.name
        )


@dataclass
class PlayerGame:
    player: Player
    position: str
    kills: int = 0
    deaths: int = 0
    assists: int = 0
    damagetochampions: int = 0
    visionscore: int = 0
    totalgold: int = 0
    golddiffat15: int = 0

    @classmethod
    def from_dict(cls, data: Dict):
        item = cls(
            Player.from_dict(data['player']),
            data['position'],
        )
        item.set_int_attrs(data)
        return item

    @classmethod
    def from_row(cls, row: Dict):
        player = Player.from_row(row)
        position = parse_str(row['position'])
        item = cls(
            player,
            position
        )
        item.set_int_attrs(row)
        return item

    def as_dict(self) -> OrderedDict:
        return OrderedDict(
            player=self.player.as_dict(),
            position=self.position,
            kills=self.kills,
            deaths=self.deaths,
            assists=self.assists,
            damagetochampions=self.damagetochampions,
            visionscore=self.visionscore,
            totalgold=self.totalgold,
            golddiffat15=self.golddiffat15
        )

    def set_int_attrs(self, data: Dict):
        for attr in ('kills', 'deaths', 'assists', 'damagetochampions', 'visionscore', 'totalgold', 'golddiffat15'):
            setattr(self, attr, parse_int(data[attr]))


@dataclass
class TeamGame:
    team: Team
    side: str
    win: bool = False
    dragons: int = 0
    elders: int = 0
    heralds: int = 0
    barons: int = 0
    towers: int = 0
    firstblood: bool = False
    firstdragon: bool = False
    firstherald: bool = False
    firstbaron: bool = False
    firsttower: bool = False

    BOOL_ATTRS = (
        'firstblood', 'firstdragon',
        'firstherald', 'firstbaron', 'firsttower'
    )

    INT_ATTRS = (
        'dragons',
        'elders',
        'heralds',
        'barons',
        'towers',
    )

    @classmethod
    def from_dict(cls, data: Dict):
        item = cls(
            Team.from_dict(data['team']),
            data['side'],
            win=parse_bool(data['win'])
        )
        item.set_int_attrs(data)
        item.set_bool_attrs(data)
        return item

    @classmethod
    def from_row(cls, row: Dict):
        team = Team.from_row(row)
        side = parse_str(row['side'])
        item = cls(
            team,
            side,
            win=parse_bool(row['result'])
        )
        item.set_int_attrs(row)
        item.set_bool_attrs(row)
        return item

    def as_dict(self) -> OrderedDict:
        return OrderedDict(
            team=self.team.as_dict(),
            side=self.side,
            win=self.win,
            **self.get_attrs()
        )

    def set_bool_attrs(self, data: Dict):
        for attr in self.BOOL_ATTRS:
            setattr(self, attr, parse_bool(data[attr]))

    def set_int_attrs(self, data: Dict):
        for attr in self.INT_ATTRS:
            setattr(self, attr, parse_int(data[attr]))

    def get_attrs(self) -> Dict:
        return dict([
            (attr, getattr(self, attr)) for attr in chain(self.INT_ATTRS, self.BOOL_ATTRS)
        ])


@dataclass
class Game:

    gameid: str
    date: datetime
    duration: int
    game: int
    league: str
    split: str
    playoffs: bool
    status: str
    playergames: List[PlayerGame] = field(init=False, default_factory=list)
    teamgames: List[TeamGame] = field(init=False, default_factory=list)

    @classmethod
    def from_row(cls, row: Dict):
        gameid = row['gameid']
        date = parse_dt(row['date'])
        duration = parse_int(row['gamelength'])
        league = parse_str(row['league'])
        split = parse_str(row['split'])
        game = parse_int(row['game'], default=1)
        position = parse_str(row['position']).lower()
        if gameid is None:
            gameid = make_game_id(league, date, game)
        game = cls(
            gameid,
            date,
            duration,
            game,
            league,
            split,
            parse_bool(row['playoffs']),
            parse_str(row['datacompleteness'])
        )
        if position == 'team':
            game.teamgames.append(TeamGame.from_row(row))
        else:
            game.playergames.append(PlayerGame.from_row(row))
        return game

    @classmethod
    def from_dict(cls, data: Dict):
        game = cls(
            data['gameid'],
            datetime.strptime(data['date'], INPUT_DT_FORMAT),
            data['duration'],
            data['game'],
            data['league'],
            data['split'],
            data['playoffs'],
            data['status']
        )
        game.playergames.extend([
            PlayerGame.from_dict(d) for d in data['playergames']
        ])
        game.teamgames.extend([
            TeamGame.from_dict(d) for d in data['teamgames']
        ])
        return game

    def as_dict(self) -> OrderedDict:
        return OrderedDict(
            gameid=self.gameid,
            date=self.date.strftime(INPUT_DT_FORMAT),
            duration=self.duration,
            game=self.game,
            league=self.league,
            split=self.split,
            playoffs=self.playoffs,
            status=self.status,
            playergames=[p.as_dict() for p in self.playergames],
            teamgames=[t.as_dict() for t in self.teamgames]
        )


class GameIterator:

    def __init__(self, rows: Iterable[Dict]):
        self.rows = rows
        self.current_game: Game = None

    def __iter__(self) -> Iterable[Game]:
        for row in self.rows:
            game: Game = Game.from_row(row)
            if self.current_game is None:
                self.current_game = game
            elif game.gameid == self.current_game.gameid:
                # same game - update the team and player games
                self.current_game.playergames.extend(game.playergames)
                self.current_game.teamgames.extend(game.teamgames)
            else:
                # its new. yield what we have
                yield self.current_game
                # start a new game
                self.current_game = game
        # don't forget the last one
        if self.current_game is not None:
            yield self.current_game
