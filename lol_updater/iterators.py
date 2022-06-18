from typing import Iterable, Dict
from datetime import datetime


class Latest:
    '''
    Wraps csv dict reader to only yield rows whose timestamp is greater than the one supplied
    '''

    def __init__(self, dt: datetime, rows: Iterable[Dict], parser, attr: str = 'date'):
        self.dt = dt
        self.parser = parser
        self.attr = attr
        self.rows = rows

    def __iter__(self) -> Iterable[Dict]:
        for row in self.rows:
            dt = self.parser(row[self.attr])
            if dt and dt > self.dt:
                yield row
