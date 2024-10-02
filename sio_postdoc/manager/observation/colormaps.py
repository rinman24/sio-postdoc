"""Custom colormaps for visualization."""

from matplotlib.colors import ListedColormap
from pydantic import BaseModel

from sio_postdoc.manager import PlotPane

SHUPE_2007: ListedColormap = ListedColormap(
    [
        "#ffffff",  # NONE
        "#033198",  # SNOW
        "#2d88be",  # ICE
        "#89dad7",  # MIXED
        "#d2d484",  # LIQUID
        "#ac7726",  # DRIZZLE
        "#7e1700",  # RAIN
    ]
)

EDGES: ListedColormap = ListedColormap(
    [
        "#389cc6",
        "#ffffff",
        "#b68c32",
    ]
)

colormaps: dict[PlotPane, ListedColormap] = {
    PlotPane.REFL: ListedColormap(
        [
            "#ffe0df",
            "#f7baaa",
            "#e3a97a",
            "#c39f4a",
            "#948f32",
            "#698040",
            "#457353",
            "#256360",
            "#155062",
            "#0f3a5f",
            "#011959",
        ]
    ),
    PlotPane.MEAN_DOPP_VEL: ListedColormap(
        [
            "#293c6f",
            "#366392",
            "#668baf",
            "#9eb5cc",
            "#d0d0a2",
            "#a6a66b",
            "#777744",
            "#4c4c20",
            "#262600",
        ]
    ),
    PlotPane.SPEC_WIDTH: ListedColormap(
        [
            "#fed3cf",
            "#e8ac86",
            "#bf9d46",
            "#7e8737",
            "#497451",
            "#205f61",
            "#114360",
            "#011959",
        ]
    ),
    PlotPane.DEPOL: ListedColormap(
        [
            "#c8b455",
            "#b3e9cd",
            "#90ded7",
            "#69c9d5",
            "#49b0ce",
            "#3597c4",
            "#297fba",
            "#2167b0",
            "#184da4",
            "#033198",
        ]
    ),
    PlotPane.TEMP: ListedColormap(
        [
            "#033198",
            "#1b54a8",
            "#2676b6",
            "#3495c3",
            "#4fb5d0",
            "#7ed5d7",
            "#afe8cf",
            "#cce7b0",
            "#d1cd78",
            "#c2a647",
            "#b2842d",
        ]
    ),
    PlotPane.STEP_1: SHUPE_2007,
    PlotPane.STEP_2: SHUPE_2007,
    PlotPane.STEP_3: SHUPE_2007,
    PlotPane.STEP_4A: SHUPE_2007,
    PlotPane.STEP_4B: SHUPE_2007,
    PlotPane.STEP_5: SHUPE_2007,
    PlotPane.STEP_6: SHUPE_2007,
    PlotPane.STEP_7: SHUPE_2007,
    PlotPane.STEP_8: SHUPE_2007,
    PlotPane.STEP_RADAR_EDGES: EDGES,
    PlotPane.STEP_LIDAR_EDGES: EDGES,
    PlotPane.STEP_OCCULTATION_ZONE: ListedColormap(
        [
            "#ffffff",
            "#7e1700",
        ]
    ),
}


class Limits(BaseModel):
    """Encapsulate colormap limits."""

    vmin: float
    vmax: float


PHASES_SHUPE_2007: Limits = Limits(vmin=-0.5, vmax=6.5)
EDGE_LIMITS: Limits = Limits(vmin=-1.5, vmax=1.5)

colormap_limits: dict[PlotPane, Limits] = {
    PlotPane.REFL: Limits(vmin=-70, vmax=40),
    PlotPane.MEAN_DOPP_VEL: Limits(vmin=-4, vmax=5),
    PlotPane.SPEC_WIDTH: Limits(vmin=0, vmax=1.6),
    PlotPane.DEPOL: Limits(vmin=0, vmax=1),
    PlotPane.TEMP: Limits(vmin=-70, vmax=40),
    PlotPane.STEP_1: PHASES_SHUPE_2007,
    PlotPane.STEP_2: PHASES_SHUPE_2007,
    PlotPane.STEP_3: PHASES_SHUPE_2007,
    PlotPane.STEP_4A: PHASES_SHUPE_2007,
    PlotPane.STEP_4B: PHASES_SHUPE_2007,
    PlotPane.STEP_5: PHASES_SHUPE_2007,
    PlotPane.STEP_6: PHASES_SHUPE_2007,
    PlotPane.STEP_7: PHASES_SHUPE_2007,
    PlotPane.STEP_8: PHASES_SHUPE_2007,
    PlotPane.STEP_RADAR_EDGES: EDGE_LIMITS,
    PlotPane.STEP_LIDAR_EDGES: EDGE_LIMITS,
    PlotPane.STEP_OCCULTATION_ZONE: Limits(vmin=-0.5, vmax=1.5),
}
