"""TODO: Docstring."""

import re

from sio_postdoc.engine.transformation.contracts import DateTime

REGEX: dict[str, str] = {
    "datetime": "D[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}-[0-9]{2}-[0-9]{2}",
    "date": "D[0-9]{4}-[0-9]{2}-[0-9]{2}",
    "month": "D[0-9]{4}-[0-9]{2}",
}
PATTERNS: dict[str, str] = {key: re.compile(value) for key, value in REGEX.items()}


def extract_datetime(
    raw: str, time: bool = True, filename_day: bool = True
) -> DateTime:
    """Extract `DateTime` from string."""
    day: int = 1
    hour: int = 0
    minute: int = 0
    second: int = 0
    if time and filename_day:
        extracted: str = PATTERNS["datetime"].search(raw).group(0)
        hour = int(extracted[12:14])
        minute = int(extracted[15:17])
        second = int(extracted[18:])
        day = int(extracted[9:11])
    elif not time and filename_day:
        extracted: str = PATTERNS["date"].search(raw).group(0)
        day = int(extracted[9:11])
    elif not time and not filename_day:
        extracted: str = PATTERNS["month"].search(raw).group(0)
    return DateTime(
        year=int(extracted[1:5]),
        month=int(extracted[6:8]),
        day=day,
        hour=hour,
        minute=minute,
        second=second,
    )
