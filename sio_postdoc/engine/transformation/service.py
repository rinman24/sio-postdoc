# pylint: disable=missing-function-docstring, missing-module-docstring, missing-class-docstring

import pandas as pd
from pydantic import BaseModel

from sio_postdoc.access.instrument.contracts import DateRange, TimeHeightData
from sio_postdoc.engine.transformation.strategies import AbstractUnpackingStrategy


class UnpackingContext:

    def __init__(self, strategy: AbstractUnpackingStrategy) -> None:
        self._strategy: AbstractUnpackingStrategy = strategy

    @property
    def strategy(self) -> AbstractUnpackingStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: AbstractUnpackingStrategy) -> None:
        self._strategy = strategy

    def unpack(self) -> None:
        return self.strategy.unpack()


# TODO: Remove all of this stuff.


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
) -> TimeHeightData:
    df: pd.DataFrame = _to_df(data)
    result = df.rolling(window, center=True).apply(func)
    return _to_contract(result, TimeHeightData)
