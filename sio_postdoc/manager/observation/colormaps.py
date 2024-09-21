"""Custom colormaps for visualization."""

from matplotlib.colors import ListedColormap
from pydantic import BaseModel

from sio_postdoc.manager import PlotPane

colormaps: dict[PlotPane, ListedColormap] = {
    # PlotPane.REFL: ListedColormap(
    #     [
    #         "#033198",
    #         "#1B54A8",
    #         "#2676B6",
    #         "#3495C3",
    #         "#4FB5D0",
    #         "#7ED5D7",
    #         "#AFE8CF",
    #         "#CCE7B0",
    #         "#D1CD78",
    #         "#C2A647",
    #         "#B2842D",
    #     ]
    # ),
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
            "#3190C1",
            "#5DC1D3",
            "#A4E5D3",
            "#D0E3A3",
            "#C8B455",
            "#B07F2A",
            "#995215",
            "#7E1700",
        ]
    ),
    # PlotPane.SPEC_WIDTH: ListedColormap(
    #     [
    #         "#cce7b2",
    #         "#d2d484",
    #         "#c8b455",
    #         "#ba9437",
    #         "#ac7726",
    #         "#9e5c19",
    #         "#903e0d",
    #         "#7e1700",
    #     ]
    # ),
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
            "#c8b455",  # "#d2d98d",
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
            "#2064ae",
            "#3190c1",
            "#5dc1d3",
            "#a4e5d3",
            "#d0e3a3",
            "#c8b455",
            "#b07f2a",
            "#995215",
        ]
    ),
}


class limits(BaseModel):
    """Encapsulate colormap limits."""

    vmin: float
    vmax: float


colormap_limits: dict[PlotPane, limits] = {
    PlotPane.REFL: limits(vmin=-70, vmax=40),
    PlotPane.MEAN_DOPP_VEL: limits(vmin=-3, vmax=5),
    PlotPane.SPEC_WIDTH: limits(vmin=0, vmax=1.6),
    PlotPane.DEPOL: limits(vmin=0, vmax=1),
    PlotPane.TEMP: limits(vmin=-50, vmax=40),
}
