from datetime import date
from pathlib import Path

import pytest

from sio_postdoc.access.instrument.contracts import InstrumentData
from sio_postdoc.access.instrument.strategies.data import DabulData, ShebaDabulRaw
from sio_postdoc.access.instrument.strategies.location import MobileLocationStrategy
from sio_postdoc.access.instrument.strategies_ import DabulInstrumentStrategy
from sio_postdoc.engine.filtering.strategies import IndicesByDate, NamesByDate
from sio_postdoc.manager.observation.service import ObservationManager


@pytest.mark.skip(reason="Troubleshooting")
def test_this_troubleshoot():
    service: ObservationManager = ObservationManager()
    # Get a tiple of all the blobs in the container
    target: date = date(1998, 1, 5)
    container: str = "sheba-dabul-raw-1998"
    blobs: tuple[str, ...] = service.instrument_access.list_blobs(container)
    # Use the NamesByDate strategy to find names of blobs as strings
    service.filtering_engine.date_context.strategy = NamesByDate()
    filtered: tuple[str, ...] = service.filtering_engine.apply(
        target=target,
        content=blobs,
    )
    # Use the site and instrument specific strategy to get a tuple of InstrumentData
    service.instrument_access.data_context.strategy = ShebaDabulRaw()
    datasets = service.instrument_access.get_data(container=container, names=filtered)
    # Use the IndicesByDate strategy to get a tuple of indices that correspont to a given day
    service.filtering_engine.date_context.strategy = IndicesByDate()
    data: InstrumentData = service.filtering_engine.apply(
        target=target,
        content=datasets,
    )
    # Now that you have a single day, in a standardized format, you can use
    # access to store the blob
    # This involved converting from InstrumentData back to netcdf.
    new_container: str = "testing-remote"
    # Use the Mobile and Dabul Strategies to create the file
    # You are here, access need the two other contexts as well.
    service.instrument_access.ncdf_context.instrument = DabulInstrumentStrategy()
    service.instrument_access.ncdf_context.location = MobileLocationStrategy()
    # service.instrument_access.push(data, new_container)
    filename: str = service.instrument_access.ncdf_context.create_file(data)
    path: Path = Path(f"./{filename}")
    # This line seems to be timing out on my computer.
    service.instrument_access.add_blob(name="testing-remote", path=path)
    # That should have written the data, let's see if it actually worked and what else we need to do to the data.


@pytest.mark.skip(reason="Troubleshooting")
def test_this_second_troubleshoot():
    service: ObservationManager = ObservationManager()
    # Get a tiple of all the blobs in the container
    target: date = date(1998, 1, 5)
    container: str = "testing-remote"
    blobs: tuple[str, ...] = service.instrument_access.list_blobs(container)
    service.filtering_engine.date_context.strategy = NamesByDate()
    filtered: tuple[str, ...] = service.filtering_engine.apply(
        target=target,
        content=blobs,
    )
    service.instrument_access.data_context.strategy = DabulData()
    datasets = service.instrument_access.get_data(container=container, names=filtered)
    x = 1


@pytest.mark.skip(reason="Troubleshooting")
def test_this_third_troubleshoot():
    service: ObservationManager = ObservationManager()
    target: date = date(year=1998, month=5, day=18)
    container: str = "sheba-dabul-raw-1998"
    blobs: tuple[str, ...] = service.instrument_access.list_blobs(container)
    service.filtering_engine.date_context.strategy = NamesByDate()
    filtered: tuple[str, ...] = service.filtering_engine.apply(
        target=target,
        content=blobs,
    )
    service.instrument_access.data_context.strategy = ShebaDabulRaw()
    datasets = service.instrument_access.get_data(container=container, names=filtered)
    service.filtering_engine.date_context.strategy = IndicesByDate()
    data: InstrumentData = service.filtering_engine.apply(
        target=target,
        content=datasets,
    )
    new_container: str = "sheba-dabul-daily-1998"
    service.instrument_access.ncdf_context.instrument = DabulInstrumentStrategy()
    service.instrument_access.ncdf_context.location = MobileLocationStrategy()
    filename: str = service.instrument_access.ncdf_context.create_file(data)
    path: Path = Path(f"./{filename}")
    service.instrument_access.add_blob(name=new_container, path=path)
