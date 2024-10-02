"""Custom facecolors for visualization."""

from sio_postdoc.manager import PlotPane

axis_facecolors: dict[PlotPane, str] = {
    PlotPane.REFL: "#ffffff",
    PlotPane.MEAN_DOPP_VEL: "#ffffff",
    PlotPane.SPEC_WIDTH: "#ffffff",
    PlotPane.DEPOL: "#ffffff",
    PlotPane.TEMP: "#ffffff",
    PlotPane.STEP_1: "#d6d6d6",
    PlotPane.STEP_2: "#d6d6d6",
    PlotPane.STEP_3: "#d6d6d6",
    PlotPane.STEP_4A: "#d6d6d6",
    PlotPane.STEP_4B: "#d6d6d6",
    PlotPane.STEP_5: "#d6d6d6",
    PlotPane.STEP_6: "#d6d6d6",
    PlotPane.STEP_7: "#d6d6d6",
    PlotPane.STEP_8: "#d6d6d6",
    PlotPane.STEP_RADAR_EDGES: "#d6d6d6",
    PlotPane.STEP_LIDAR_EDGES: "#d6d6d6",
    PlotPane.STEP_OCCULTATION_ZONE: "#d6d6d6",
}
