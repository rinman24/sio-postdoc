from datetime import date
from pathlib import Path

from sio_postdoc.access.instrument.contracts import InstrumentData
from sio_postdoc.access.instrument.strategies import (
    DabulInstrumentStrategy,
    MobileLocationStrategy,
    ShebaDabulRaw,
)
from sio_postdoc.engine.filtering.strategies import IndicesByDate, NamesByDate
from sio_postdoc.manager.observation.service import ObservationManager


def test_troubleshoot():
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
    assert False
    # But the filter needs to return a single set of instrument data
    # That has only timestamps for that day.
    assert isinstance(data, InstrumentData)
    print(datasets)
