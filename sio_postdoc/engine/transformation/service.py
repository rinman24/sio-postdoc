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
) -> TimeHeightData:
    df: pd.DataFrame = _to_df(data)
    result = df.rolling(window, center=True).apply(func)
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
