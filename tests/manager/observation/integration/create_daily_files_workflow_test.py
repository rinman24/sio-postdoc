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

# Here is how you process several years of raw data
# STEP 1: run the months in parallel
# YEARS = [2020, 2021, 2022]
# OBSERVATORY = Observatory.OLIKTOK
# products = [Product.ARSCLKAZR1KOLLIAS, Product.INTERPOLATEDSONDE, Product.MPLCMASKML]
# for year in YEARS:
#     for month in [Month.JAN]:
#         for product in products:
#             request = DailyProductRequest(
#                 product=product,
#                 observatory=OBSERVATORY,
#                 month=month,
#                 year=year,
#             )
#             manager.create_daily_product_files(request)
#         request = ObservatoryRequest(
#             observatory=OBSERVATORY,
#             month=month,
#             year=year,
#         )
#         manager.create_daily_resampled_merged_files(request)
#         manager.create_daily_layers_and_phases(request)
#         manager.reclassify_mixed_columns(request)
#         manager.create_monthly_phase_summary(request)

# STEP 2: Summarize Annually
# for year in YEARS:
#     request = ObservatoryRequest(
#         observatory=OBSERVATORY,
#         month=None,
#         year=year,
#     )
#     manager.create_annual_phase_summary(request)
#     manager.create_annual_phase_summary_by_temp(request)
#     manager.create_annual_phase_summary_for_report(request)
#     manager.create_annual_phase_summary_for_report_2(request)


# for year in [2019]:
#     request = ObservatoryRequest(
#         observatory=Observatory.UTQIAGVIK,
#         month=None,
#         year=year,
#     )
#     manager.create_annual_phase_summary_for_report_2(request)


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
        product=Product.INTERPOLATEDSONDE,
        observatory=Observatory.UTQIAGVIK,
        month=Month.JAN,
        year=2023,
    )
    manager.create_daily_product_files(request)


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_create_daily_resampled_merged_files(manager):
    request = ObservatoryRequest(
        observatory=Observatory.UTQIAGVIK,
        month=Month.MAR,
        year=2023,
    )
    manager.create_daily_resampled_merged_files(request)


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_create_daily_layers_and_phases(manager):
    request = ObservatoryRequest(
        observatory=Observatory.UTQIAGVIK,
        month=Month.MAR,
        year=2023,
    )
    manager.create_daily_layers_and_phases(request)


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_reclassify_mixed_columns(manager):
    request = ObservatoryRequest(
        observatory=Observatory.UTQIAGVIK,
        month=Month.MAR,
        year=2023,
    )
    manager.reclassify_mixed_columns(request)


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_create_monthly_phase_summary(manager):
    request = ObservatoryRequest(
        observatory=Observatory.UTQIAGVIK,
        month=Month.MAR,
        year=2023,
    )
    manager.create_monthly_phase_summary(request)


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_create_annual_phase_summary(manager):
    request = ObservatoryRequest(
        observatory=Observatory.UTQIAGVIK,
        month=Month.MAR,
        year=2023,
    )
    manager.create_annual_phase_summary(request)


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_create_annual_phase_summary_by_temp(manager):
    request = ObservatoryRequest(
        observatory=Observatory.UTQIAGVIK,
        month=None,
        year=2023,
    )
    manager.create_annual_phase_summary_by_temp(request)


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_create_annual_phase_summary_for_report(manager):
    request = ObservatoryRequest(
        observatory=Observatory.UTQIAGVIK,
        month=None,
        year=2023,
    )
    manager.create_annual_phase_summary_for_report(request)


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_create_annual_correlation_timeseries(manager):
    request = ObservatoryRequest(
        observatory=Observatory.UTQIAGVIK,
        month=None,
        year=2023,
    )
    manager.create_annual_correlation_timeseries(request)


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_create_annual_phase_summary_for_report_2(manager):
    request = ObservatoryRequest(
        observatory=Observatory.UTQIAGVIK,
        month=Month.MAR,
        year=2023,
    )
    manager.create_annual_phase_summary_for_report_2(request)


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_create_monthly_elevation_by_phase(manager):
    request = ObservatoryRequest(
        observatory=Observatory.UTQIAGVIK,
        month=Month.JAN,
        year=2023,
    )
    manager.create_monthly_elevation_by_phase(request)


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
