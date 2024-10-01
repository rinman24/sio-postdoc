"""Custom plot labels."""

from sio_postdoc.manager import PlotPane

BLACK: str = "#000000"
DLR: str = r"$\dot{E}_{\ell \hspace{-0.3} \downarrow} \hspace{-0.8}^{''}\hspace{0.8}$"
HEIGHT: str = "Height [km, AGL]"
LWP: str = r"$m^{''}$"

plot_labels: dict[PlotPane, str] = {
    PlotPane.MEAN_DOPP_VEL: r"Radar Mean Doppler Velocity, $V_D$",
    PlotPane.REFL: r"Radar Reflectivity, $Z_e$",
    PlotPane.SPEC_WIDTH: r"Radar Spectral Width, $W_D$",
    PlotPane.DEPOL: r"Lidar Depolarization Ratio, $\delta$",
    PlotPane.LWP: rf"Liquid Water Path, {LWP}",
    PlotPane.DLR: rf"Downwelling Longwave Radiation, {DLR}",
    PlotPane.TEMP: r"Atmospheric Temperature, $T$",
    PlotPane.STEP_1: "Step 1",
    PlotPane.STEP_2: "Step 2",
    PlotPane.STEP_3: "Step 3",
    PlotPane.STEP_4A: "Step 4(a)",
    PlotPane.STEP_RADAR_TOPS: "Radar Tops",
    PlotPane.STEP_LIDAR_TOPS: "Lidar Tops",
    PlotPane.STEP_OCCULTATION_ZONE: "Occultation Zone",
    PlotPane.STEP_4B: "Step 4(b)",
    PlotPane.STEP_5: "Step 5",
    PlotPane.STEP_6: "Step 6",
    PlotPane.STEP_7: "Step 7",
    PlotPane.STEP_8: "Step 8",
}

plot_label_colors: dict[PlotPane, str] = {
    PlotPane.MEAN_DOPP_VEL: BLACK,
    PlotPane.REFL: BLACK,
    PlotPane.SPEC_WIDTH: BLACK,
    PlotPane.DEPOL: BLACK,
    PlotPane.LWP: BLACK,
    PlotPane.DLR: BLACK,
    PlotPane.TEMP: BLACK,
    PlotPane.STEP_1: BLACK,
    PlotPane.STEP_2: BLACK,
    PlotPane.STEP_3: BLACK,
    PlotPane.STEP_4A: BLACK,
    PlotPane.STEP_RADAR_TOPS: BLACK,
    PlotPane.STEP_LIDAR_TOPS: BLACK,
    PlotPane.STEP_OCCULTATION_ZONE: BLACK,
    PlotPane.STEP_4B: BLACK,
    PlotPane.STEP_5: BLACK,
    PlotPane.STEP_6: BLACK,
    PlotPane.STEP_7: BLACK,
    PlotPane.STEP_8: BLACK,
}

plot_ylabels: dict[PlotPane, str] = {
    PlotPane.MEAN_DOPP_VEL: HEIGHT,
    PlotPane.REFL: HEIGHT,
    PlotPane.SPEC_WIDTH: HEIGHT,
    PlotPane.DEPOL: HEIGHT,
    PlotPane.LWP: rf"{LWP} [g/m$^2$]",
    PlotPane.DLR: rf"{DLR} [W/m$^2$]",
    PlotPane.TEMP: HEIGHT,
    PlotPane.STEP_1: HEIGHT,
    PlotPane.STEP_2: HEIGHT,
    PlotPane.STEP_3: HEIGHT,
    PlotPane.STEP_4A: HEIGHT,
    PlotPane.STEP_RADAR_TOPS: HEIGHT,
    PlotPane.STEP_LIDAR_TOPS: HEIGHT,
    PlotPane.STEP_OCCULTATION_ZONE: HEIGHT,
    PlotPane.STEP_4B: HEIGHT,
    PlotPane.STEP_5: HEIGHT,
    PlotPane.STEP_6: HEIGHT,
    PlotPane.STEP_7: HEIGHT,
    PlotPane.STEP_8: HEIGHT,
}
