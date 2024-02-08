import re
from calendar import monthrange
from collections import defaultdict
from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import Union

import netCDF4 as ncdf

from sio_postdoc.access.instrument.constants import DATADIR, MONTH_DIRECTORIES
from sio_postdoc.access.instrument.contracts import (
    DateRange,
    DayRange,
    FilterRequest,
    LidarData,
    MonthRange,
    RawDataRequest,
    RawDataResponse,
    RawTimeHeightData,
    TimeHeightData,
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


def _locate_previous(
    month: int,
    year: int,
    current_path: Path,
) -> RawDataResponse:
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
    return RawDataResponse(
        paths=[file],
        datetimes=[_extract_datetime(file, int(year))],
    )


def _filter_files(request: FilterRequest) -> list[Path]:
    paths: list[Path] = list(request.response.paths)
    datetimes: list[datetime] = list(request.response.datetimes)
    files: list[Path] = _get_files(request.path, ext="ncdf", sort=True)
    this_datetime: Union[None, datetime]
    for i, file in enumerate(files):
        this_datetime = _extract_datetime(file, request.year)
        if this_datetime is None:
            continue
        if this_datetime.day in request.valid_days:
            if this_datetime == request.start:
                paths.append(file)
                datetimes.append(this_datetime)
                continue
            elif request.start < this_datetime and this_datetime < request.end:
                if len(paths) == 0:
                    if i == 0:
                        previous_response: RawDataResponse = _locate_previous(
                            this_datetime.month,
                            request.year,
                            request.path,
                        )
                        previous_file = previous_response.paths[0]
                        previous_datetime = previous_response.datetimes[0]
                    else:
                        previous_file = files[i - 1]
                        previous_datetime = _extract_datetime(
                            previous_file, request.year
                        )
                    paths.append(previous_file)
                    datetimes.append(previous_datetime)
                paths.append(file)
                datetimes.append(this_datetime)
            elif this_datetime == request.end:
                paths.append(file)
                datetimes.append(this_datetime)
                break
        if this_datetime > request.end:
            paths.append(file)
            datetimes.append(this_datetime)
            break
    return RawDataResponse(paths=paths, datetimes=datetimes)


def _identify_files(request: RawDataRequest) -> RawDataResponse:
    datadir: Path = Path(DATADIR / request.location / request.instr_name)
    day_rng: DayRange = _identify_days(request.daterange)
    response: RawDataResponse = RawDataResponse(
        paths=[],
        datetimes=[],
    )

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
                response=response,
            )
            response = _filter_files(filter_request)
    return response


def _initial_datetime(dataset: ncdf.Dataset, datetime_: datetime) -> datetime:
    hours: float = float(dataset["time"][0].data)
    delta: float = hours / 24
    date_: date = datetime_.date()
    reference: datetime = datetime.combine(date_, time(0))
    initial_datetime: datetime = reference + timedelta(delta)
    return initial_datetime


def _get_datetime_indexes(
    dataset: ncdf.Dataset,
    name_datetime: datetime,
) -> list[datetime]:
    initial_datetime: datetime = _initial_datetime(dataset, name_datetime)
    results: list[datetime] = [initial_datetime]
    buffer: int = 0
    for i, hour in enumerate(dataset["time"][1:].data):
        previous_hour: float = float(dataset["time"][i].data)
        if hour < previous_hour:
            buffer = 24
        delta = ((hour - previous_hour) + buffer) / 24
        buffer = 0
        results.append(results[i] + timedelta(delta))
    return results


def _concatinate_raw_data(files: RawDataResponse) -> RawTimeHeightData:
    kwargs: dict[str:TimeHeightData] = dict()
    for variable in ["far_parallel", "depolarization"]:
        datetimes: list[datetime] = list()
        elevations: list[float] = list()
        values: list[list[float]] = list()
        for path, datetime_ in zip(files.paths, files.datetimes):
            dataset: ncdf.Dataset = ncdf.Dataset(path)
            datetimes += _get_datetime_indexes(dataset, datetime_)
            this_elevation = [i / 1000 for i in dataset["range"][:].data]
            values += [row.tolist() for row in dataset[variable][:].data]
            if len(elevations) == 0:
                elevations = this_elevation
            elif this_elevation != elevations:
                raise ValueError("elevations do not match across files.")

        kwargs[variable] = TimeHeightData(
            datetimes=datetimes,
            elevations=elevations,
            values=values,
        )
    return LidarData(**kwargs)
