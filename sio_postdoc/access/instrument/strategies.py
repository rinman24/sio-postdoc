import dataclasses
import re
from abc import ABC, abstractmethod
from datetime import datetime

import netCDF4 as nc

import sio_postdoc.utility.service as utility
from sio_postdoc.access.instrument.contracts import (
    InstrumentData,
    PhysicalMatrix,
    PhysicalVector,
    TemporalVector,
)

FLAG: float = float(-999)
SECONDS_PER_DAY: int = 86400


class AbstractDataStrategy(ABC):
    """TODO: docstring."""

    @abstractmethod
    def extract(self, name: str) -> InstrumentData: ...

    @staticmethod
    def monotonic_times(times: list[float], units: str):
        # Convert to seconds (potentially non-monotonic)
        scale: int
        match units:
            case "hours":
                scale = 3600
        seconds = [round(i * scale) for i in times]

        # Convert to monotonic seconds
        previous: float = float(FLAG)  # Large negative number
        datum: int = 0  # Initially on same day
        monotonic_seconds: list[float] = []
        for item in seconds:
            if item < previous:
                datum += SECONDS_PER_DAY
            monotonic_seconds.append(int(datum + item))
            previous = item
        return tuple(monotonic_seconds)


class Default(AbstractDataStrategy):

    def extract(self, name: str) -> InstrumentData:
        """TODO: Implement."""


class ShebaDabulRaw(AbstractDataStrategy):

    def extract(self, name: str) -> InstrumentData:
        dataset = nc.Dataset(name)
        initial_datetime: datetime = utility.extract_datetime(name)
        prefix: str = utility.extract_prefix(name)
        suffix: str = utility.extract_suffix(name)
        notes: str = ""
        if prefix and suffix:
            notes = f"{prefix}.{suffix}"
        elif not prefix:
            notes = f"{suffix}"
        elif not suffix:
            notes = f"{prefix}"
        offsets: list[float] = [float(i) for i in dataset["time"]]
        seconds: tuple[int, ...] = self.monotonic_times(offsets, units="hours")
        time: TemporalVector = TemporalVector(
            initial=initial_datetime,
            offsets=seconds,
            units="seconds",
            name="seconds since initial time",
            scale=1,
            flag=-999,
        )
        axis: PhysicalVector = PhysicalVector(
            values=(float(i) for i in dataset["range"]),
            units="meters",
            name="range",
            scale=1,
            flag=-999,
        )
        vectors: list[PhysicalVector] = []
        for variable in (
            "latitude",
            "longitude",
            "altitude",
            "elevation",
            "azimuth",
            "scanmode",
        ):
            name: str = variable
            value_type: type = float
            flag: int = -999
            scale: int = 1
            match variable:
                case "latitude":
                    units = "degrees north"
                case "longitude":
                    units = "degrees east"
                case "altitude":
                    units = "meters"
                case "elevation":
                    units = "degrees"
                    name = "beam elevation angle"
                case "azimuth":
                    units = "degrees"
                    name = "beam azimuth angle"
                case "scanmode":
                    units = "none"
                    name = "scan mode"
                    value_type = int
            values: tuple[int | float, ...] = tuple(
                value_type(i) for i in dataset[variable]
            )
            vector: PhysicalVector = PhysicalVector(
                values=values,
                units=units,
                name=name,
                scale=scale,
                flag=flag,
            )
            vectors.append(vector)

        matrices: list[PhysicalMatrix] = []
        for variable in ("depolarization", "far_parallel"):
            name: str = variable
            values: list[list[float]] = []
            for row in dataset[variable]:
                values.append(tuple(float(i) for i in row))
            flag: int = -999
            scale: int = 1
            match variable:
                case "depolarization":
                    name = "depolarization ratio"
                    units = "none"
                case "far_parallel":
                    name = "far parallel"
                    units = "unknown"
            matrix: PhysicalMatrix = PhysicalMatrix(
                values=tuple(values),
                units=units,
                name=name,
                scale=scale,
                flag=flag,
            )
            matrices.append(matrix)

        result: InstrumentData = InstrumentData(
            time=time,
            axis=(axis,),
            matrices=tuple(matrices),
            vectors=tuple(vectors),
            name="dabul",
            observatory="SHEBA",
            notes=notes,
        )

        return result


class AbstractLocationStrategy(ABC):
    """This class is responsible for handling the location specifics."""

    @abstractmethod
    def write_data(self, data: InstrumentData, rootgrp: nc.Dataset) -> nc.Dataset: ...


class MobileLocationStrategy(AbstractLocationStrategy):

    def write_data(self, data: InstrumentData, rootgrp: nc.Dataset) -> nc.Dataset:
        """TODO: Implement"""
        dimension: tuple[str] = ("record",)
        latitude = rootgrp.createVariable("latitude", "f4", dimension)
        longitude = rootgrp.createVariable("longitute", "f4", dimension)
        altitude = rootgrp.createVariable("altitude", "f4", dimension)
        # TODO: you need to make all of the flagged data -999 at some point.
        for vector in data.vectors:
            match vector.name:
                case "latitude":
                    latitude[:] = list(vector.values)
                case "longitude":
                    longitude[:] = list(vector.values)
                case "altitude":
                    altitude[:] = list(vector.values)
        return rootgrp


class StationaryLocationStrategy(AbstractLocationStrategy):

    def write_data(self, data: InstrumentData, rootgrp: nc.Dataset) -> nc.Dataset:
        """TODO: Implement"""


class AbstractInstrumentStrategy(ABC):

    @abstractmethod
    def write_data(self, data: InstrumentData, rootgrp: nc.Dataset) -> nc.Dataset: ...


class DabulInstrumentStrategy(AbstractInstrumentStrategy):

    def write_data(self, data: InstrumentData, rootgrp: nc.Dataset) -> nc.Dataset:
        """TODO: Implement"""
        # One and two dimensions
        dimension: tuple[str] = ("record",)
        dimensions: tuple[str, str] = ("record", "level")
        # Vectors
        elevation = rootgrp.createVariable("elevation", "f4", dimension)
        azimuth = rootgrp.createVariable("azimuth", "f4", dimension)
        scan_mode = rootgrp.createVariable("scan_mode", "f4", dimension)
        # TODO: you need to make all of the flagged data -999 at some point.
        for vector in data.vectors:
            match vector.name:
                case "beam elevation angle":
                    elevation[:] = list(vector.values)
                case "beam azimuth angle":
                    azimuth[:] = list(vector.values)
                case "scan mode":
                    scan_mode[:] = list(vector.values)
        # Matrices
        depolarization = rootgrp.createVariable("depolarization", "f4", dimensions)
        parallel = rootgrp.createVariable("parallel", "f4", dimensions)
        for matrix in data.matrices:
            match matrix.name:
                case "depolarization ratio":
                    depolarization[:] = matrix.values
                case "far parallel":
                    parallel[:] = matrix.values
        return rootgrp


class MmcrInstrumentStrategy(AbstractInstrumentStrategy):

    def write_data(self, data: InstrumentData, rootgrp: nc.Dataset) -> nc.Dataset:
        """TODO: Implement"""
