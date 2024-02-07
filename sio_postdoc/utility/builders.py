from datetime import datetime
from typing import Union

from sio_postdoc.access.instrument.contracts import (
    DateRange,
    Instrument,
    RawDataRequest,
)


class AccessContractsBuilder:

    @staticmethod
    def get_datetime(input_: str) -> datetime:
        input_ = input_.replace("-", "").replace(":", "")
        kwargs: dict[str, int] = dict(
            year=int(input_[:4]),
            month=int(input_[4:6]),
            day=int(input_[6:8]),
            hour=int(input_[8:10]),
            minute=int(input_[10:12]),
        )
        return datetime(**kwargs)

    def daterange(self, start: str, end: str) -> DateRange:
        kwargs: dict[str, datetime] = dict(
            start=self.get_datetime(start),
            end=self.get_datetime(end),
        )

        return DateRange(**kwargs)

    def instrument(self, location: str, name: str) -> Instrument:
        return Instrument(location=location, name=name)

    def raw_data_request(
        self,
        start: str,
        end: str,
        location: str,
        name: str,
    ) -> RawDataRequest:
        kwargs: dict[str, Union[DateRange, Instrument]] = dict(
            daterange=self.daterange(start, end),
            instrument=self.instrument(location, name),
        )
        return RawDataRequest(**kwargs)
