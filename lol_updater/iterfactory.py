import csv
from datetime import datetime

from . import iterators
from . import parsers


def csv_latest_iterator(latest: datetime, input) -> iterators.Latest:
    return iterators.Latest(
        latest,
        csv.DictReader(input),
        parsers.parse_dt
    )


def csv_game_iterator(latest: datetime, input):
    return parsers.GameIterator(csv_latest_iterator(latest, input))
