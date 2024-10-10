"""Test the create daily files workflow."""

from pathlib import Path

import pytest
from dotenv import load_dotenv

from sio_postdoc.engine.transformation.wavelet import TopHat
from sio_postdoc.manager import (
    Instrument,
    Month,
    Observatory,
    Process,
    Product,
    Wavelet,
    WaveletOrder,
)
from sio_postdoc.manager.observation.contracts import (
    DailyProductRequest,
    DailyRequest,
    ObservatoryRequest,
    ProcessPlotRequest,
    ProcessRequest,
)
from sio_postdoc.manager.observation.service import ObservationManager

# load_dotenv(override=True)
# manager: ObservationManager = ObservationManager()


@pytest.fixture(scope="module")
def manager() -> ObservationManager:
    """Yield module level service for testing."""
    load_dotenv(override=True)
    return ObservationManager()


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_format_dir(manager: ObservationManager):
    directory: Path = Path(
        "C:\\Users\\sio-admin\\Desktop\\data\\utqiagvik\\kazr\\2019\\nsaarsclkazr1kolliasC1.c0.20190101.000000.nc"
    )
    manager.format_dir(directory=directory, suffix=".nc", year="2019")


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_process_plot_request(manager: ObservationManager):
    request = ProcessPlotRequest(
        observatory=Observatory.UTQIAGVIK,
        year=2022,
        month=Month.OCT,
        day=6,
        process=Process.RESAMPLE,
        # top=6,
    )
    manager.process(request)


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_monthly_phase_fractions(manager: ObservationManager):
    request = ProcessRequest(
        observatory=Observatory.UTQIAGVIK,
        month=Month.OCT,
        year=2022,
        process=Process.MONTHLY,
    )
    manager.process(request)


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_process_normalized_phases(manager: ObservationManager):
    request = ProcessRequest(
        observatory=Observatory.UTQIAGVIK,
        month=Month.OCT,
        year=2022,
        process=Process.NORMALIZE_PHASES,
        seconds=int(5 * 60),
        meters=1000,
    )
    manager.process(request)


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_process_monthly_phases(manager: ObservationManager):
    request = ProcessRequest(
        observatory=Observatory.UTQIAGVIK,
        month=Month.OCT,
        year=2022,
        process=Process.MONTHLY_TIMESERIES,
        seconds=int(5 * 60),
        meters=1000,
    )
    manager.process(request)


def test_top_hat():
    th1 = TopHat(j=1)
    assert th1.len() == 4
    assert th1.norm() == 0.5
    assert th1.values() == (
        -0.5,
        0.5,
        0.5,
        -0.5,
    )
    th3 = TopHat(j=3)
    assert th3.len() == 16
    assert th3.norm() == 0.25
    assert th3.values() == (
        -0.25,
        -0.25,
        -0.25,
        -0.25,
        0.25,
        0.25,
        0.25,
        0.25,
        0.25,
        0.25,
        0.25,
        0.25,
        -0.25,
        -0.25,
        -0.25,
        -0.25,
    )


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_process_wavelet_two(manager: ObservationManager):
    request = ProcessRequest(
        observatory=Observatory.UTQIAGVIK,
        month=Month.OCT,
        year=2022,
        process=Process.MONTHLY_WAVELET,
        seconds=int(5 * 60),
        meters=1000,
        wavelet=Wavelet.TOP_HAT,
        wavelet_order=WaveletOrder.TWO,
    )
    manager.process(request)


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_create_daily_files(manager: ObservationManager):
    request = DailyRequest(
        instrument=Instrument.KAZR,
        observatory=Observatory.UTQIAGVIK,
        month=Month.JAN,
        year=2019,
    )
    manager.create_daily_files(request)


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_create_daily_product_files(manager: ObservationManager):
    request = DailyProductRequest(
        product=Product.INTERPOLATEDSONDE,
        observatory=Observatory.UTQIAGVIK,
        month=Month.JAN,
        year=2023,
    )
    manager.create_daily_product_files(request)


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_create_daily_resampled_merged_files(manager: ObservationManager):
    request = ProcessRequest(
        observatory=Observatory.UTQIAGVIK,
        month=Month.MAR,
        year=2022,
        process=Process.RESAMPLE,
    )
    manager.process(request)


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_add_temp_to_resampled_files(manager: ObservationManager):
    request = ProcessRequest(
        observatory=Observatory.UTQIAGVIK,
        month=Month.MAR,
        year=2022,
        process=Process.RESAMPLE,
    )
    manager._temp_add_sonde(request)


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_process_phase_request(manager: ObservationManager):
    request = ProcessRequest(
        observatory=Observatory.UTQIAGVIK,
        year=2022,
        month=Month.OCT,
        process=Process.PHASES,
    )
    manager.process(request)


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_process_reclassify_request(manager: ObservationManager):
    request = ProcessRequest(
        observatory=Observatory.UTQIAGVIK,
        year=2022,
        month=Month.SEP,
        process=Process.RECLASSIFY,
    )
    manager.process(request)


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_process_isolate_phases(manager: ObservationManager):
    request = ProcessRequest(
        observatory=Observatory.UTQIAGVIK,
        year=2022,
        month=Month.OCT,
        process=Process.ISOLATE,
    )
    manager.process(request)


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_create_daily_resampled_lwp_dlr_files(manager: ObservationManager):
    request = ObservatoryRequest(
        observatory=Observatory.UTQIAGVIK,
        month=Month.OCT,
        year=2020,
    )
    manager.create_daily_resampled_lwp_dlr_files(request)


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_create_daily_layers_and_phases(manager: ObservationManager):
    request = ObservatoryRequest(
        observatory=Observatory.UTQIAGVIK,
        month=Month.MAR,
        year=2023,
    )
    manager.create_daily_layers_and_phases(request)


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_reclassify_mixed_columns(manager: ObservationManager):
    request = ObservatoryRequest(
        observatory=Observatory.UTQIAGVIK,
        month=Month.MAR,
        year=2023,
    )
    manager.reclassify_mixed_columns(request)


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_create_monthly_phase_summary(manager: ObservationManager):
    request = ObservatoryRequest(
        observatory=Observatory.UTQIAGVIK,
        month=Month.MAR,
        year=2023,
    )
    manager.create_monthly_phase_summary(request)


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_create_annual_structure_summary(manager: ObservationManager):
    request = ObservatoryRequest(
        observatory=Observatory.UTQIAGVIK,
        month=None,
        year=2023,
    )
    manager.create_annual_structure_summary(request)


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_create_annual_phase_summary(manager: ObservationManager):
    request = ObservatoryRequest(
        observatory=Observatory.UTQIAGVIK,
        month=Month.MAR,
        year=2023,
    )
    manager.create_annual_phase_summary(request)


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_create_annual_phase_summary_by_temp(manager: ObservationManager):
    request = ObservatoryRequest(
        observatory=Observatory.UTQIAGVIK,
        month=None,
        year=2023,
    )
    manager.create_annual_phase_summary_by_temp(request)


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_create_annual_phase_summary_for_report(manager: ObservationManager):
    request = ObservatoryRequest(
        observatory=Observatory.UTQIAGVIK,
        month=None,
        year=2023,
    )
    manager.create_annual_phase_summary_for_report(request)


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_create_annual_correlation_timeseries(manager: ObservationManager):
    request = ObservatoryRequest(
        observatory=Observatory.UTQIAGVIK,
        month=None,
        year=2023,
    )
    manager.create_annual_correlation_timeseries(request)


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_create_annual_phase_summary_for_report_2(manager: ObservationManager):
    request = ObservatoryRequest(
        observatory=Observatory.UTQIAGVIK,
        month=Month.MAR,
        year=2023,
    )
    manager.create_annual_phase_summary_for_report_2(request)


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_create_monthly_elevation_by_phase(manager: ObservationManager):
    request = ObservatoryRequest(
        observatory=Observatory.UTQIAGVIK,
        month=Month.JAN,
        year=2023,
    )
    manager.create_monthly_elevation_by_phase(request)


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_create_daily_masks(manager: ObservationManager):
    request = DailyRequest(
        instrument=Instrument.MMCR,
        observatory=Observatory.SHEBA,
        month=Month.NOV,
        year=1997,
    )
    manager.create_daily_masks(request, threshold=-5, name="refl")


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_create_daily_layer_plots(manager: ObservationManager):
    request = DailyRequest(
        instrument=Instrument.KAZR,
        observatory=Observatory.UTQIAGVIK,
        month=Month.JAN,
        year=2019,
    )
    manager.create_daily_layer_plots(request)


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_create_annual_lwp_ts(manager: ObservationManager):
    request = ObservatoryRequest(
        observatory=Observatory.UTQIAGVIK,
        year=2022,
    )
    manager.create_annual_lwp_ts(request)
