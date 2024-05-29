"""Test the create daily files workflow."""

from pathlib import Path

import pytest
from dotenv import load_dotenv

from sio_postdoc.manager import Instrument, Month, Observatory, Product
from sio_postdoc.manager.observation.contracts import (
    DailyProductRequest,
    DailyRequest,
    ObservatoryRequest,
)
from sio_postdoc.manager.observation.service import ObservationManager

# load_dotenv(override=True)
# manager = ObservationManager()

# for month in [
#     Month.JAN,
#     Month.FEB,
#     Month.MAR,
#     Month.APR,
#     Month.MAY,
#     Month.JUN,
#     Month.JUL,
#     Month.AUG,
#     Month.SEP,
#     Month.OCT,
#     Month.NOV,
#     Month.DEC,
# ]:
#     request = DailyProductRequest(
#         product=Product.ARSCLKAZR1KOLLIAS,
#         observatory=Observatory.UTQIAGVIK,
#         month=month,
#         year=2023,
#     )
#     manager.create_daily_product_files(request)


# for month in [Month.AUG, Month.SEP, Month.OCT, Month.NOV, Month.DEC]:
#     request = DailyRequest(
#         instrument=Instrument.KAZR,
#         observatory=Observatory.UTQIAGVIK,
#         month=month,
#         year=2019,
#     )
#     manager.create_daily_layer_plots(request)


# directory: Path = Path("C:\\Users\\sio-admin\\Desktop\\data\\utqiagvik\\mpl\\2019")
# manager.format_dir(directory=directory, suffix=".cdf", year="2019")

# request = ObservatoryRequest(
#     observatory=Observatory.SHEBA,
#     month=Month.SEP,
#     year=1998,
# )
# manager.merge_daily_masks(request)


# request = DailyRequest(
#     instrument=Instrument.MMCR,
#     observatory=Observatory.SHEBA,
#     month=Month.NOV,
#     year=1998,
# )
# manager.create_daily_masks(request)


# for month in [Month.JAN, Month.FEB, Month.MAR, Month.APR, Month.MAY, Month.JUN, Month.JUL, Month.AUG, Month.SEP, Month.OCT, Month.NOV, Month.DEC]:
#     request = DailyRequest(
#         instrument=Instrument.MMCR,
#         observatory=Observatory.EUREKA,
#         month=month,
#         year=2014,
#     )
#     manager.create_daily_files(request)


@pytest.fixture(scope="module")
def manager() -> ObservationManager:
    """Yield module level service for testing."""
    load_dotenv(override=True)
    return ObservationManager()


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_format_dir(manager):
    directory: Path = Path(
        "C:\\Users\\sio-admin\\Desktop\\data\\utqiagvik\\kazr\\2019\\nsaarsclkazr1kolliasC1.c0.20190101.000000.nc"
    )
    manager.format_dir(directory=directory, suffix=".nc", year="2019")


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_create_daily_files(manager):
    request = DailyRequest(
        instrument=Instrument.KAZR,
        observatory=Observatory.UTQIAGVIK,
        month=Month.JAN,
        year=2019,
    )
    manager.create_daily_files(request)


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_create_daily_product_files(manager):
    request = DailyProductRequest(
        product=Product.MPLCMASKML,
        observatory=Observatory.UTQIAGVIK,
        month=Month.JAN,
        year=2023,
    )
    manager.create_daily_product_files(request)


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_create_daily_masks(manager):
    request = DailyRequest(
        instrument=Instrument.MMCR,
        observatory=Observatory.SHEBA,
        month=Month.NOV,
        year=1997,
    )
    manager.create_daily_masks(request, threshold=-5, name="refl")


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_create_daily_layer_plots(manager):
    request = DailyRequest(
        instrument=Instrument.KAZR,
        observatory=Observatory.UTQIAGVIK,
        month=Month.JAN,
        year=2019,
    )
    manager.create_daily_layer_plots(request)
