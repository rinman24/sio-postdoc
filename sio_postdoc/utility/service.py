"""TODO: Docstring."""

import re

from sio_postdoc.engine.transformation.contracts import DateTime, InstrumentData

REGEX: str = "D[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}-[0-9]{2}-[0-9]{2}"
PATTERN = re.compile(REGEX)


def extract_datetime(raw: str) -> DateTime:
    """Extract `DateTime` from string."""
    extracted: str = PATTERN.search(raw).group(0)
    return DateTime(
        year=int(extracted[1:5]),
        month=int(extracted[6:8]),
        day=int(extracted[9:11]),
        hour=int(extracted[12:14]),
        minute=int(extracted[15:17]),
        second=int(extracted[18:]),
    )


def extract_suffix(raw: str) -> str:
    """TODO: Docstring."""
    match: re.Match = PATTERN.search(raw)
    tail: str = raw[match.end() :]
    suffix: str = ".".join(tail.lstrip(".").split(".")[:-1])
    return suffix


def extract_prefix(raw: str) -> str:
    """TODO: Docstring."""
    match: re.Match = PATTERN.search(raw)
    prefix: str = raw[: match.start()].rstrip(".")
    return prefix


def get_filename(data: InstrumentData) -> str:
    """TODO: Docstring."""
    year: str = str(data.time.initial.year)
    month: str = str(data.time.initial.month).zfill(2)
    day: str = str(data.time.initial.day).zfill(2)
    hour: str = str(data.time.initial.hour).zfill(2)
    minute: str = str(data.time.initial.minute).zfill(2)
    second: str = str(data.time.initial.second).zfill(2)

    result: str = f"D{year}-{month}-{day}T{hour}-{minute}-{second}.{data.notes}.nc"
    return result
