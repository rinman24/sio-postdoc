from typing import Optional

import pandas as pd
from pydantic import BaseModel

from sio_postdoc.access.instrument.contracts import DateRange, TimeHeightData


def _to_df(data: TimeHeightData) -> pd.DataFrame:
    return pd.DataFrame(
        data.values,
        index=data.datetimes,
        columns=data.elevations,
    )


def _to_contract(df: pd.DataFrame, contract: BaseModel) -> BaseModel:
    if contract is TimeHeightData:
        return TimeHeightData(
            datetimes=df.index.to_pydatetime().tolist(),
            elevations=df.columns.values.tolist(),
            values=[i.tolist() for i in df.to_numpy()],
        )


def _replace(
    data: TimeHeightData,
    flag: float,
    value: float,
) -> TimeHeightData:
    df: pd.DataFrame = _to_df(data)
    df = df.replace(flag, value)
    return _to_contract(df, TimeHeightData)


def _crop(data: TimeHeightData, range: DateRange) -> TimeHeightData:
    df: pd.DataFrame = _to_df(data)
    mask: list[bool] = (
        (range.start <= df.index) & (df.index <= range.end)
    ).tolist()  # noqa
    df = df[mask]
    return _to_contract(df, TimeHeightData)


def _rolling_apply(
    data: TimeHeightData,
    func: object,
    window: str,
    kwargs: Optional[dict] = None,
) -> TimeHeightData:
    df: pd.DataFrame = _to_df(data)
    result = df.rolling(window, center=True).apply(func, kwargs=kwargs)
    return _to_contract(result, TimeHeightData)


def _top_hat(j: int) -> list[float]:
    tau: float
    length: int = 2**j
    scale: float = 1 / (2 ** (j + 1)) ** 0.5
    result: list[float] = list()
    for i in range(length):
        tau = i / length
        if (tau < 0.25) or (tau >= 0.75):
            result.append(-scale)
        else:
            result.append(scale)
    return result


def _wavelet(values, kind) -> float:
    # TODO: Use a match case instead
    if kind == "tophat":
        length: int = len(values)
        valid_lengths: set = set([4, 8, 16, 32, 64, 128, 256])
        j_lookup: dict[int, int] = {
            4: 2,
            8: 3,
            16: 4,
            32: 5,
            64: 6,
            128: 7,
            256: 8,
        }
        if length in valid_lengths:
            j: int = j_lookup[length]
            return sum(th * f for th, f in zip(_top_hat(j), values))
    else:
        raise ValueError(f"'{kind}' is not a valed wavelet option")


def _periodogram(data: TimeHeightData, j: int) -> TimeHeightData:
    # TODO: this j is trickey here, make sure you don't mix this up later
    df: pd.DataFrame = _to_df(data)
    df = (df**2) / (2 ** (j + 1))
    return _to_contract(df, TimeHeightData)
