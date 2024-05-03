"""Transformation Context Service."""

from datetime import date
from pathlib import Path

from sio_postdoc.access import DataSet
from sio_postdoc.engine.transformation.contracts import InstrumentData
from sio_postdoc.engine.transformation.strategies.base import TransformationStrategy
from sio_postdoc.manager.observation.contracts import DailyRequest, ObservatoryRequest


class TransformationContext:
    """Encapsulate the interface of interest for transformations."""

    def __init__(self) -> None:
        """Initialize the `TransformationContext`."""
        self.strategy: None | TransformationStrategy = None

    def hydrate(self, dataset: DataSet, path: Path) -> InstrumentData:
        """Use the strategy to hydrate an instance of `InstrumentData`."""
        return self.strategy.hydrate(dataset, path)

    def serialize(
        self, target: date, data: InstrumentData, request: DailyRequest
    ) -> Path:
        """Use `InstrumentData` to write a `DataSet` to the `path`."""
        filepath: Path = Path.cwd() / (
            f"D{target.year}"
            f"-{str(target.month).zfill(2)}"
            f"-{str(target.day).zfill(2)}"
            f"-{request.observatory.name.lower()}"
            f"-{request.instrument.name.lower()}"
            ".ncdf"
        )
        # Attributes
        dataset: DataSet = DataSet(filepath, "w", format="NETCDF4")
        dataset.instrument = request.instrument.name
        dataset.observatory = request.observatory.name
        # Dimensions
        for name, dimension in data.dimensions.items():
            dataset.createDimension(name, dimension.size)
        # Variables
        for name, variable in data.variables.items():
            current = dataset.createVariable(
                name,
                variable.dtype.name.lower(),
                tuple(dim.name.name.lower() for dim in variable.dimensions),
            )
            current.long_name = variable.long_name
            current._scale = variable.scale.value
            current.units = variable.units.name
            current[:] = variable.values
        dataset.close()
        return filepath

    def serialize_mask(
        self, target: date, data: InstrumentData, request: ObservatoryRequest
    ) -> Path:
        """Use `InstrumentData` to write a `DataSet` to the `path`."""
        filepath: Path = Path.cwd() / (
            f"D{target.year}"
            f"-{str(target.month).zfill(2)}"
            f"-{str(target.day).zfill(2)}"
            f"-{request.observatory.name.lower()}"
            ".ncdf"
        )
        # Attributes
        dataset: DataSet = DataSet(filepath, "w", format="NETCDF4")
        dataset.observatory = request.observatory.name
        # Dimensions
        for name, dimension in data.dimensions.items():
            dataset.createDimension(name, dimension.size)
        # Variables
        for name, variable in data.variables.items():
            current = dataset.createVariable(
                name,
                variable.dtype.name.lower(),
                tuple(dim.name.name.lower() for dim in variable.dimensions),
            )
            current.long_name = variable.long_name
            current._scale = variable.scale.value
            current.units = variable.units.name
            current[:] = variable.values
        dataset.close()
        return filepath
