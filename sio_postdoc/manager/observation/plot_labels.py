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
    PlotPane.STEP_1: "Step 1: Lidar Identification of Liquid and Ice (Depolarization Ratio)",
    PlotPane.STEP_2: "Step 2: Radar Identification of Drizzle and Mixed-Phase in Lidar Pixels",
    PlotPane.STEP_3: "Step 3: Radar Identification of Unambiguous, Strong Precipitation",
    PlotPane.STEP_4A: "Step 4a: Radar Identification of Thermodynamic Phase",
    PlotPane.STEP_RADAR_EDGES: "Radar Edges",
    PlotPane.STEP_LIDAR_EDGES: "Lidar Edges",
    PlotPane.STEP_OCCULTATION_ZONE: "Lidar Occultation Zone",
    PlotPane.STEP_4B: "Step 4b: Ignore Spectrum Width Within Lidar Occultation Zone",
    PlotPane.STEP_5: "Step 5: Absolute Temperature Rules",
    PlotPane.STEP_6: "Step 6: Liquid Water Path Constraints",
    PlotPane.STEP_7: "Step 7: Coherence Filter",
    PlotPane.STEP_8: "Step 8: Classification Rules",
    PlotPane.REFERENCE: "Classification from Shupe (2007)",
    PlotPane.RENUMBERED: "Conversion to Classes from Shupe (2011)",
    PlotPane.MODIFIED_MIXED: "Mixed-Phase Classification from Shupe (2011)",
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
    PlotPane.STEP_RADAR_EDGES: BLACK,
    PlotPane.STEP_LIDAR_EDGES: BLACK,
    PlotPane.STEP_OCCULTATION_ZONE: BLACK,
    PlotPane.STEP_4B: BLACK,
    PlotPane.STEP_5: BLACK,
    PlotPane.STEP_6: BLACK,
    PlotPane.STEP_7: BLACK,
    PlotPane.STEP_8: BLACK,
    PlotPane.REFERENCE: BLACK,
    PlotPane.RENUMBERED: BLACK,
    PlotPane.MODIFIED_MIXED: BLACK,
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
    PlotPane.STEP_RADAR_EDGES: HEIGHT,
    PlotPane.STEP_LIDAR_EDGES: HEIGHT,
    PlotPane.STEP_OCCULTATION_ZONE: HEIGHT,
    PlotPane.STEP_4B: HEIGHT,
    PlotPane.STEP_5: HEIGHT,
    PlotPane.STEP_6: HEIGHT,
    PlotPane.STEP_7: HEIGHT,
    PlotPane.STEP_8: HEIGHT,
    PlotPane.REFERENCE: HEIGHT,
    PlotPane.RENUMBERED: HEIGHT,
    PlotPane.MODIFIED_MIXED: HEIGHT,
}
