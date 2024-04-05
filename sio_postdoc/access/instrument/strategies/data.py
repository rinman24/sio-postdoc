"""Strategies to construct InstrumentData from netCDF4.Datasets."""

from datetime import datetime
from typing import Protocol

import netCDF4 as nc

import sio_postdoc.utility.service as utility
from sio_postdoc.access.instrument.constants import REFERENCE_TIME
from sio_postdoc.access.instrument.contracts import (
    InstrumentData,
    PhysicalMatrix,
    PhysicalVector,
    TemporalVector,
)
from sio_postdoc.access.instrument.strategies.constants import (
    ShebaDabulRawMatrixParams,
    ShebaDabulRawVectorParams,
    ShebaMmcrRawMatrixParams,
)
from sio_postdoc.access.instrument.strategies.contracts import RawDataParams

FLAG: float = float(-999)
SECONDS_PER_DAY: int = 86400
FLAGS: dict[str, int] = {
    "S1": 0,
    "u2": 2**16 - 1,
    "i2": int(-(2**16) / 2),
    "i4": -999,
    "f4": -999,
}

Dataset = nc.Dataset


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


def _monotonic_times(times: list[float], units: str) -> tuple[int, ...]:
    """TODO: Docstring."""
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


class InstrumentDataStrategy(Protocol):
    """Define protocol for constructing InstrumentData."""

    def extract(self, name: str) -> InstrumentData: ...  # noqa: D102


class ShebaDabulRaw(InstrumentDataStrategy):
    """TODO: Docstring."""

    vector_params: dict[str, RawDataParams] = ShebaDabulRawVectorParams
    matrix_params: dict[str, RawDataParams] = ShebaDabulRawMatrixParams

    @staticmethod
    def _construct_time(name: str, dataset: Dataset) -> TemporalVector:
        initial_datetime: datetime = utility.extract_datetime(name)
        base_time: int = int((initial_datetime - REFERENCE_TIME).total_seconds())
        offsets: list[float] = [float(i) for i in dataset["time"]]
        time: TemporalVector = TemporalVector(
            base_time=base_time,
            offsets=_monotonic_times(offsets, units="hours"),
            units="seconds",
            name="offsets",
            long_name="Seconds Since Initial Time",
            scale=1,
            flag=FLAGS["i4"],
            dtype="i4",
        )
        return time

    @staticmethod
    def _construct_axis(dataset: Dataset) -> TemporalVector:
        # Axis
        axis: PhysicalVector = PhysicalVector(
            values=tuple(int(i) for i in dataset["range"]),
            units="meters",
            name="range",
            long_name="Height of Measured Value; agl",
            scale=1,
            flag=FLAGS["u2"],
            dtype="u2",
        )
        return axis

    @staticmethod
    def _construct_vectors(dataset: Dataset) -> dict[str, PhysicalVector]:
        params: RawDataParams
        vectors: dict[str, PhysicalVector] = {}
        for variable in ShebaDabulRaw.vector_params.keys():
            params = ShebaDabulRaw.vector_params[variable]
            values: tuple[int, ...] = tuple(
                (
                    int(element * params.scale)
                    if params.valid_range.min
                    <= element * params.scale
                    <= params.valid_range.max
                    else params.flag
                )
                for element in dataset[variable][:]
            )
            vector: PhysicalVector = PhysicalVector(
                values=values,
                units=params.units,
                name=params.name,
                long_name=params.long_name,
                scale=params.scale,
                flag=params.flag,
                dtype=params.dtype,
            )
            vectors[variable] = vector
        return vectors

    @staticmethod
    def _construct_matrices(dataset: Dataset) -> dict[str, PhysicalMatrix]:
        params: RawDataParams
        matrices: dict[str, PhysicalMatrix] = {}
        for variable in ShebaDabulRaw.matrix_params.keys():
            params = ShebaDabulRaw.matrix_params[variable]
            values: list[list[int]] = []
            for row in dataset[variable][:]:
                values.append(
                    tuple(
                        (
                            int(element * params.scale)
                            if params.valid_range.min
                            <= element * params.scale
                            <= params.valid_range.max
                            else params.flag
                        )
                        for element in row[:]
                    )
                )
            matrix: PhysicalMatrix = PhysicalMatrix(
                values=tuple(values),
                units=params.units,
                name=params.name,
                long_name=params.long_name,
                scale=params.scale,
                flag=params.flag,
                dtype=params.dtype,
            )
            matrices[params.name] = matrix
        return matrices

    def extract(self, name: str) -> InstrumentData:
        """Extract raw SHEBA DABUL data."""
        dataset: Dataset = Dataset(name)
        notes: str = _get_notes(name)
        time: TemporalVector = self._construct_time(name, dataset)
        axis: PhysicalVector = self._construct_axis(dataset)
        vectors: dict[str, PhysicalVector] = self._construct_vectors(dataset)
        matrices: dict[str, PhysicalMatrix] = self._construct_matrices(dataset)
        result: InstrumentData = InstrumentData(
            time=time,
            axis=axis,
            matrices=matrices,
            vectors=vectors,
            name="DABUL",
            observatory="SHEBA",
            notes=notes,
        )
        return result


class ShebaMmcrRaw(InstrumentDataStrategy):
    """TODO: Docstring."""

    matrix_params: dict[str, RawDataParams] = ShebaMmcrRawMatrixParams

    @staticmethod
    def _construct_time(dataset: Dataset) -> TemporalVector:
        base_time: int = int(dataset["base_time"][0])
        offsets: list[float] = [float(i) for i in dataset["time_offset"]]
        time: TemporalVector = TemporalVector(
            base_time=base_time,
            offsets=_monotonic_times(offsets, units="seconds"),
            units="seconds",
            name="offsets",
            long_name="Seconds Since Initial Time",
            scale=1,
            flag=-999,
            dtype="i4",
        )
        return time

    @staticmethod
    def _construct_axis(dataset: Dataset) -> TemporalVector:
        axis: PhysicalVector = PhysicalVector(
            values=tuple(int(i) for i in dataset["Heights"]),
            units="meters",
            name="range",
            long_name="Height of Measured Value; agl",
            scale=1,
            flag=FLAGS["u2"],
            dtype="u2",
        )
        return axis

    @staticmethod
    def _construct_matrices(dataset: Dataset) -> dict[str, PhysicalMatrix]:
        params: RawDataParams
        matrices: dict[str, PhysicalMatrix] = {}
        for variable in ShebaMmcrRaw.matrix_params.keys():
            params = ShebaMmcrRaw.matrix_params[variable]
            values: list[list[int]] = []
            for row in dataset[variable][:]:
                values.append(
                    tuple(
                        (
                            params.strategy(element) * params.scale
                            if params.valid_range.min
                            <= params.strategy(element) * params.scale
                            <= params.valid_range.max
                            else params.flag
                        )
                        for element in row[:]
                    )
                )
            matrix: PhysicalMatrix = PhysicalMatrix(
                values=tuple(values),
                units=params.units,
                name=params.name,
                long_name=params.long_name,
                scale=params.scale,
                flag=params.flag,
                dtype=params.dtype,
            )
            matrices[params.name] = matrix
        return matrices

    def extract(self, name: str) -> InstrumentData:
        """Extract raw SHEBA MMCR data."""
        dataset = Dataset(name)
        notes: str = _get_notes(name)
        time: TemporalVector = self._construct_time(dataset)
        axis: PhysicalVector = self._construct_axis(dataset)
        matrices: list[PhysicalMatrix] = self._construct_matrices(dataset)
        result: InstrumentData = InstrumentData(
            time=time,
            axis=axis,
            matrices=matrices,
            vectors={},  # No Vectors
            name="MMCR",
            observatory="SHEBA",
            notes=notes,
        )
        return result
