import re
from datetime import datetime

from sio_postdoc.access.instrument.contracts import InstrumentData

REGEX: str = "D[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}-[0-9]{2}-[0-9]{2}"
PATTERN = re.compile(REGEX)


def extract_datetime(raw: str) -> datetime:
    """TODO: docstring."""
    extracted: str = PATTERN.search(raw).group(0)
    return datetime(
        year=int(extracted[1:5]),
        month=int(extracted[6:8]),
        day=int(extracted[9:11]),
        hour=int(extracted[12:14]),
        minute=int(extracted[15:17]),
        second=int(extracted[18:]),
    )


def extract_suffix(raw: str) -> str:
    match: re.Match = PATTERN.search(raw)
    tail: str = raw[match.end() :]
    suffix: str = "".join(tail.split(".")[:-1])
    return suffix


def extract_prefix(raw: str) -> str:
    match: re.Match = PATTERN.search(raw)
    prefix: str = raw[: match.start()]
    return prefix


def get_filename(data: InstrumentData) -> str:
    year: str = str(data.time.initial.year)
    month: str = str(data.time.initial.month).zfill(2)
    day: str = str(data.time.initial.day).zfill(2)
    hour: str = str(data.time.initial.hour).zfill(2)
    minute: str = str(data.time.initial.minute).zfill(2)
    second: str = str(data.time.initial.second).zfill(2)

    result: str = f"D{year}-{month}-{day}T{hour}-{minute}-{second}.{data.notes}.nc"
    return result
