import re
from calendar import monthrange
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Union

from sio_postdoc.access.instrument.constants import DATADIR, MONTH_DIRECTORIES
from sio_postdoc.access.instrument.contracts import (
    DateRange,
    DayRange,
    FilterRequest,
    MonthRange,
    RawDataRequest,
)


def _identify_years(range: DateRange) -> list[int]:
    return sorted(
        set(
            [
                range.start.year,
                range.end.year,
            ]
        )
    )


def _identify_months(range: DateRange) -> MonthRange:
    years: list[int] = _identify_years(range)
    months: dict[int, list[int]] = {year: [] for year in years}

    year: int = years[0]
    month: int = range.start.month

    final_month: bool = False
    while not final_month:
        months[year].append(month)
        if (year == range.end.year) and (month == range.end.month):
            final_month = True
        else:
            if month == 12:
                month = 1
                year += 1
            else:
                month += 1

    return MonthRange(years=years, months=months)


def _identify_days(range: DateRange) -> DayRange:
    month_rng: MonthRange = _identify_months(range)
    days: dict[str, list[int]] = defaultdict(list)

    day: int = range.start.day
    final_day: bool = False

    for year in month_rng.years:
        for month in sorted(month_rng.months[year]):
            last_day_of_month: int = monthrange(year, month)[1]
            while (not final_day) and (day <= last_day_of_month):
                days[f"{year}-{month}"].append(day)
                if (
                    (year == range.end.year)
                    and (month == range.end.month)
                    and (day == range.end.day)
                ):
                    final_day = True
                elif day == last_day_of_month:
                    day = 1
                    break
                else:
                    day += 1

    return DayRange(
        years=month_rng.years,
        months=month_rng.months,
        days=days,
    )


def _extract_datetime(file: Path, year: int):
    filename: str = str(file)
    pattern: re.Pattern = re.compile("[0-9]{8}")
    search_result: Union[None, re.Match] = pattern.search(filename)
    if search_result is None:
        return None
    start: int = search_result.start()
    end: int = search_result.end()
    match_: str = filename[start:end]
    kwargs: dict[str, int] = dict(
        year=year,
        month=int(match_[0:2]),
        day=int(match_[2:4]),
        hour=int(match_[4:6]),
        minute=int(match_[6:8]),
    )
    result: datetime = datetime(**kwargs)
    return result


def _get_files(path: Path, ext: str, sort: bool) -> list[Path]:
    result: list[Path]
    result = [path for path in path.iterdir() if path.suffix == ".ncdf"]
    if sort:
        return sorted(result)
    return result


def _locate_previous(month: int, year: int, current_path: Path) -> list[Path]:
    path: Path
    if month == 1:
        year: str = f"{year - 1}"
        month: str = MONTH_DIRECTORIES[12]
    else:
        year: str = str(year)
        month: str = MONTH_DIRECTORIES[month - 1]
    path: Path = current_path.parents[1] / year / month
    files: list[Path] = _get_files(path, ext="ncdf", sort=True)
    file: Path = files[-1]
    return file


def _filter_files(request: FilterRequest) -> list[Path]:
    result: list[Path] = list(request.identified)
    files: list[Path] = _get_files(request.path, ext="ncdf", sort=True)
    this_datetime: Union[None, datetime]
    for i, file in enumerate(files):
        this_datetime = _extract_datetime(file, request.year)
        if this_datetime is None:
            continue
        if this_datetime.day in request.valid_days:
            if this_datetime == request.start:
                result.append(file)
                continue
            elif request.start < this_datetime and this_datetime < request.end:
                if len(result) == 0:
                    if i == 0:
                        previous_file: Path = _locate_previous(
                            this_datetime.month,
                            request.year,
                            request.path,
                        )
                    else:
                        previous_file = files[i - 1]
                    result.append(previous_file)
                result.append(file)
            elif this_datetime == request.end:
                result.append(file)
                break
        if this_datetime > request.end:
            result.append(file)
            break
    return result


def _identify_files(request: RawDataRequest) -> list[Path]:
    datadir: Path = Path(DATADIR / request.location / request.instr_name)
    day_rng: DayRange = _identify_days(request.daterange)
    identified: list[Path] = list()

    for year in day_rng.years:
        yeardir = datadir / str(year)
        for month in sorted(day_rng.months[year]):
            filedir = yeardir / MONTH_DIRECTORIES[month]
            filter_request: FilterRequest = FilterRequest(
                start=request.start,
                end=request.end,
                path=filedir,
                valid_days=day_rng.days[f"{year}-{month}"],
                year=year,
                identified=identified,
            )
            identified = _filter_files(filter_request)
    return identified
