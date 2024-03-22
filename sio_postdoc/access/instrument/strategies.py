import dataclasses
import re
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Callable

import netCDF4 as nc

import sio_postdoc.utility.service as utility
from sio_postdoc.access.instrument.contracts import (
    InstrumentData,
    PhysicalMatrix,
    PhysicalVector,
    TemporalVector,
)

FLAG: float = float(-999)
REF_DATE: datetime = datetime(1970, 1, 1, 0, 0)
SECONDS_PER_DAY: int = 86400
FLAGS: dict[str, int] = {
    "S1": 0,
    "i2": int(-(2**16) / 2),
    "f4": -999,
}
METHODS: dict[str, Callable] = {
    "S1": int.from_bytes,
    "i2": int,
    "f4": float,
}


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
            case "seconds":
                scale = 1
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

    @staticmethod
    def _get_notes(name: str) -> str:
        prefix: str = utility.extract_prefix(name)
        suffix: str = utility.extract_suffix(name)
        notes: str = ""
        if prefix and suffix:
            notes = f"{prefix}.{suffix}"
        elif not prefix:
            notes = f"{suffix}"
        elif not suffix:
            notes = f"{prefix}"
        return notes


class Default(AbstractDataStrategy):

    def extract(self, name: str) -> InstrumentData:
        """TODO: Implement."""


class ShebaDabulRaw(AbstractDataStrategy):
    variable_names: tuple[str] = (
        "latitude",
        "longitude",
        "altitude",
        "elevation",
        "azimuth",
        "scanmode",
    )
    matrix_names: tuple[str] = (
        "depolarization",
        "far_parallel",
    )

    def extract(self, name: str) -> InstrumentData:
        # Open the nc file
        dataset = nc.Dataset(name)
        # Extract initial timestamp and notes for the filename.
        initial_datetime: datetime = utility.extract_datetime(name)
        notes: str = self._get_notes(name)
        # Construct the Temporal Vector
        offsets: list[float] = [float(i) for i in dataset["time"]]
        time: TemporalVector = TemporalVector(
            initial=initial_datetime,
            offsets=self.monotonic_times(offsets, units="hours"),
            units="seconds",
            name="seconds since initial time",
            scale=1,
            flag=FLAGS["i2"],
            dtype="i2",
        )
        axis: PhysicalVector = PhysicalVector(
            values=tuple(float(i) for i in dataset["range"]),
            units="meters",
            name="range",
            scale=1,
            flag=FLAGS["i2"],
            dtype="i2",
        )
        # Vectors
        vectors: list[PhysicalVector] = []
        for variable in self.variable_names:
            units: str
            dtype: str
            scale: int
            scale: int
            match variable:
                case "latitude":
                    units = "degrees north"
                    dtype = "f4"
                    scale = 1
                case "longitude":
                    units = "degrees east"
                    dtype = "f4"
                    scale = 1
                case "altitude":
                    units = "meters"
                    dtype = "f4"
                    scale = 1
                case "elevation":
                    units = "degrees"
                    dtype = "f4"
                    scale = 1
                case "azimuth":
                    units = "degrees"
                    dtype = "f4"
                    scale = 1
                case "scanmode":
                    units = "none"
                    dtype = "i2"
                    scale = 1
            values: tuple[int | float, ...] = tuple(
                METHODS[dtype](i) for i in dataset[variable]
            )
            vector: PhysicalVector = PhysicalVector(
                values=values,
                units=units,
                name=variable,
                scale=scale,
                flag=FLAGS["f4"],
                dtype=dtype,
            )
            vectors.append(vector)

        matrices: list[PhysicalMatrix] = []
        for variable in self.matrix_names:
            scale: int
            units: str
            dtype: str
            scale: int
            match variable:
                case "depolarization":
                    units = "none"
                    dtype = "f4"
                    scale = 1
                case "far_parallel":
                    units = "unknown"
                    dtype = "f4"
                    scale = 1
            values: list[list[int | float]] = []
            for row in dataset[variable]:
                values.append(tuple(METHODS[dtype](i) for i in row))

            matrix: PhysicalMatrix = PhysicalMatrix(
                values=tuple(values),
                units=units,
                name=variable,
                scale=scale,
                flag=FLAGS[dtype],
                dtype=dtype,
            )
            matrices.append(matrix)

        result: InstrumentData = InstrumentData(
            time=time,
            axis=(axis,),
            matrices=tuple(matrices),
            vectors=tuple(vectors),
            name="DABUL",
            observatory="SHEBA",
            notes=notes,
        )

        return result


class ShebaMmcrRaw(AbstractDataStrategy):
    matrix_names: tuple[str] = (
        "Qc",
        "Reflectivity",
        "MeanDopplerVelocity",
        "SpectralWidth",
        "ModeId",
        "SignaltoNoiseRatio",
    )
    matrix_map: dict[str, str] = dict(
        Qc="qc",
        Reflectivity="reflectivity",
        MeanDopplerVelocity="mean_doppler_velocity",
        SpectralWidth="spectral_width",
        ModeId="mode_id",
        SignaltoNoiseRatio="signal_to_noise_ratio",
    )

    def extract(self, name: str) -> InstrumentData:
        # Open the nc file
        dataset = nc.Dataset(name)
        # Extract initial timestamp and notes for the filename.
        base_time: int = int(dataset["base_time"][0])
        initial_datetime: datetime = REF_DATE + timedelta(seconds=base_time)
        notes: str = self._get_notes(name)
        # Construct the Temporal Vector
        offsets: list[float] = [float(i) for i in dataset["time_offset"]]
        time: TemporalVector = TemporalVector(
            initial=initial_datetime,
            offsets=self.monotonic_times(offsets, units="seconds"),
            units="seconds",
            name="seconds since initial time",
            scale=1,
            flag=FLAGS["i2"],
            dtype="i2",
        )
        axis: PhysicalVector = PhysicalVector(
            values=tuple(int(i) for i in dataset["Heights"]),
            units="meters",
            name="range",
            # long_name="Height of Measured Value; agl"
            scale=1,
            flag=FLAGS["i2"],
            dtype="i2",
        )
        # Vectors
        # Matrices
        matrices: list[PhysicalMatrix] = []
        for variable in self.matrix_names:
            scale: int
            units: str
            dtype: str
            scale: int
            match variable:
                case "Qc":
                    units = "none"
                    # notes = (
                    #     "Quality Control Flags: 0 - No Data, "
                    #     "1 - Good Data, "
                    #     "2 - Second Trip Echo Problems, "
                    #     "3 - Coherent Integration Problems, "
                    #     "4 - Second Trip Echo and Coherent Integration Problems"
                    # )
                    dtype = "S1"
                    scale = 1
                case "Reflectivity":
                    units = "dBZ"
                    dtype = "i2"
                    scale = 100
                case "MeanDopplerVelocity":
                    units = "m/s"
                    dtype = "i2"
                    scale = 1000
                case "SpectralWidth":
                    units = "m/s"
                    dtype = "i2"
                    scale = 1000
                case "ModeId":
                    units = "none"
                    dtype = "S1"
                    scale = 1
                case "SignaltoNoiseRatio":
                    units = "dB"
                    dtype = "i2"
                    scale = 100

            values: list[list[int | float]] = []
            for row in dataset[variable]:
                values.append(tuple(METHODS[dtype](i) for i in row))

            matrix: PhysicalMatrix = PhysicalMatrix(
                values=tuple(values),
                units=units,
                name=self.matrix_map[variable],
                scale=scale,
                flag=FLAGS[dtype],
                dtype=dtype,
            )
            matrices.append(matrix)

        result: InstrumentData = InstrumentData(
            time=time,
            axis=(axis,),
            matrices=tuple(matrices),
            vectors=tuple(),  # No Vectors
            name="MMCR",
            observatory="SHEBA",
            notes=notes,
        )

        return result


class DabulData(AbstractDataStrategy):

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
        offsets: list[float] = [float(i) for i in dataset["offsets"]]
        # seconds: tuple[int, ...] = self.monotonic_times(offsets, units="hours")
        time: TemporalVector = TemporalVector(
            initial=initial_datetime,
            offsets=offsets,
            units="seconds",
            name="seconds since initial time",
            scale=1,
            flag=-999,
        )
        axis: PhysicalVector = PhysicalVector(
            values=tuple(float(i) for i in dataset["range"]),
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
        dimension: tuple[str] = ("record",)
        latitude = rootgrp.createVariable("latitude", "f4", dimension)
        longitude = rootgrp.createVariable("longitude", "f4", dimension)
        altitude = rootgrp.createVariable("altitude", "f4", dimension)
        for vector in data.vectors:
            match vector.name:
                case "latitude":
                    latitude[:] = list(vector.values)
                    latitude.units = vector.units
                    latitude.name_ = vector.name
                    latitude.scale_ = vector.scale
                    latitude.flag = vector.flag
                case "longitude":
                    longitude[:] = list(vector.values)
                    longitude.units = vector.units
                    longitude.name_ = vector.name
                    longitude.scale_ = vector.scale
                    longitude.flag = vector.flag
                case "altitude":
                    altitude[:] = list(vector.values)
                    altitude.units = vector.units
                    altitude.name_ = vector.name
                    altitude.scale_ = vector.scale
                    altitude.flag = vector.flag
        return rootgrp


class StationaryLocationStrategy(AbstractLocationStrategy):

    def write_data(self, data: InstrumentData, rootgrp: nc.Dataset) -> nc.Dataset:
        """TODO: Implement"""


class AbstractInstrumentStrategy(ABC):
    @abstractmethod
    def write_data(self, data: InstrumentData, rootgrp: nc.Dataset) -> nc.Dataset: ...


class DabulInstrumentStrategy(AbstractInstrumentStrategy):

    def write_data(self, data: InstrumentData, rootgrp: nc.Dataset) -> nc.Dataset:
        # One and two dimensions
        dimension: tuple[str] = ("record",)
        dimensions: tuple[str, str] = ("record", "level")
        # Vectors
        elevation = rootgrp.createVariable("elevation", "f4", dimension)
        azimuth = rootgrp.createVariable("azimuth", "f4", dimension)
        scanmode = rootgrp.createVariable("scanmode", "i2", dimension)
        for vector in data.vectors:
            match vector.name:
                case "beam elevation angle":
                    elevation[:] = list(vector.values)
                    elevation.units = vector.units
                    elevation.name_ = vector.name
                    elevation.scale_ = vector.scale
                    elevation.flag = vector.flag
                case "beam azimuth angle":
                    azimuth[:] = list(vector.values)
                    azimuth.units = vector.units
                    azimuth.name_ = vector.name
                    azimuth.scale_ = vector.scale
                    azimuth.flag = vector.flag
                case "scan mode":
                    scanmode[:] = list(vector.values)
                    scanmode.units = vector.units
                    scanmode.name_ = vector.name
                    scanmode.scale_ = vector.scale
                    scanmode.flag = vector.flag
        # Matrices
        depolarization = rootgrp.createVariable("depolarization", "f4", dimensions)
        far_parallel = rootgrp.createVariable("far_parallel", "f4", dimensions)
        for matrix in data.matrices:
            match matrix.name:
                case "depolarization ratio":
                    depolarization[:] = matrix.values
                    depolarization.units = matrix.units
                    depolarization.name_ = matrix.name
                    depolarization.scale_ = matrix.scale
                    depolarization.flag = matrix.flag
                case "far parallel":
                    far_parallel[:] = matrix.values
                    far_parallel.units = matrix.units
                    far_parallel.name_ = matrix.name
                    far_parallel.scale_ = matrix.scale
                    far_parallel.flag = matrix.flag

        return rootgrp


class MmcrInstrumentStrategy(AbstractInstrumentStrategy):

    def write_data(self, data: InstrumentData, rootgrp: nc.Dataset) -> nc.Dataset:
        """TODO: Implement"""
