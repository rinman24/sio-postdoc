"""Date Formatting Strategies."""

import dataclasses
import re
from abc import ABC, abstractmethod

MONTH_MAP: dict[str, str] = dict(
    jan="01",
    feb="02",
    mar="03",
    apr="04",
    may="05",
    jun="06",
    jul="07",
    aug="08",
    sep="09",
    oct="10",
    nov="11",
    dec="12",
)


@dataclasses.dataclass
class Date:
    """Container for a date components."""

    year: str
    month: str
    day: str


@dataclasses.dataclass
class Time:
    """Container for a time components."""

    hour: str
    minute: str
    second: str


@dataclasses.dataclass
class DateTime:
    """Combination of date and time dataclasses."""

    date: Date
    time: Time


@dataclasses.dataclass
class Decomposition:
    """Decomposition of a raw string into prefix, target, and suffix."""

    prefix: str
    target: str
    suffix: str


class AbstractDateStrategy(ABC):
    """Abstract Base Class for stratigies to extended."""

    @abstractmethod
    def __init__(self) -> None:
        self.pattern: re.Pattern

    def decompose(self, raw: str) -> Decomposition:
        """Decompose the raw input into components."""
        match: re.Match = self.pattern.search(raw)
        try:
            prefix: str = raw[: match.start()]
            target: str = match.group(0)
            suffix: str = raw[match.end() :]
        except AttributeError as exc:
            raise ValueError(f"No match found: '{raw}'") from exc
        return Decomposition(
            prefix=prefix,
            target=target,
            suffix=suffix,
        )

    @abstractmethod
    def extract_time(self, raw: str, prefix: str) -> DateTime:
        """Delegated to strategies."""

    def format(self, raw: str, prefix: str) -> str:
        """Format the raw input."""
        decomposition: Decomposition = self.decompose(raw)
        datetime: DateTime = self.extract_time(decomposition.target, prefix)
        date: str = f"{datetime.date.year}-{datetime.date.month}-{datetime.date.day}"
        time: str = (
            f"{datetime.time.hour}-{datetime.time.minute}-{datetime.time.second}"
        )
        target: str = f"D{date}T{time}"
        return f"{decomposition.prefix}{target}{decomposition.suffix}"


class MMDDhhmm(AbstractDateStrategy):
    """MMSShhmm strategy which requires year prefix and assumes zero seconds."""

    def __init__(self) -> None:
        self.pattern = re.compile("[0-9]{8}")

    def extract_time(self, raw: str, prefix: str) -> DateTime:
        """Concrete Implementation of date strategy."""
        date: Date = Date(
            year=prefix,
            month=raw[:2],
            day=raw[2:4],
        )

        time: Time = Time(
            hour=raw[4:6],
            minute=raw[6:],
            second="00",
        )

        return DateTime(date=date, time=time)


class YYYYMMDDdothhmmss(AbstractDateStrategy):
    """YYYYMMDDdothhmmss strategy."""

    def __init__(self) -> None:
        self.pattern = re.compile("[0-9]{8}.[0-9]{6}")

    def extract_time(self, raw: str, _: str) -> DateTime:
        """Concrete Implementation of date strategy."""
        date: Date = Date(
            year=raw[:4],
            month=raw[4:6],
            day=raw[6:8],
        )

        time: Time = Time(
            hour=raw[9:11],
            minute=raw[11:13],
            second=raw[13:],
        )

        return DateTime(date=date, time=time)


class DDMMMYYYYdothhColonmmDashhhColonmm(AbstractDateStrategy):
    """DDMMMYYYYdothhColonmmDashhhColonmm strategy."""

    def __init__(self) -> None:
        self.pattern = re.compile(
            "[0-9]{2}[a-z]{3}[0-9]{4}.[0-9]{2}:[0-9]{2}-[0-9]{2}:[0-9]{2}"
        )

    def extract_time(self, raw: str, _: str) -> DateTime:
        """Concrete Implementation of date strategy."""
        date: Date = Date(
            year=raw[5:9],
            month=MONTH_MAP[raw[2:5]],
            day=raw[:2],
        )

        time: Time = Time(
            hour=raw[10:12],
            minute=raw[13:15],
            second="00",
        )

        return DateTime(date=date, time=time)
