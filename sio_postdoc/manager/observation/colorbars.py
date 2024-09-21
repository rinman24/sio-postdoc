"""Custom colorbars for visualizations."""

from sio_postdoc.manager import PlotPane

colorbar_extend: dict[PlotPane, str] = {
    PlotPane.MEAN_DOPP_VEL: "both",
    PlotPane.REFL: "both",
    PlotPane.SPEC_WIDTH: "max",
    PlotPane.DEPOL: "neither",
    PlotPane.TEMP: "both",
}

colorbar_labels: dict[PlotPane, str] = {
    PlotPane.MEAN_DOPP_VEL: r"$V_D$, [m/s] (positive: up)",
    PlotPane.REFL: r"$Z_e$, [dBZ]",
    PlotPane.SPEC_WIDTH: r"$W_D$, [m/s]",
    PlotPane.DEPOL: r"$\delta$",
    PlotPane.TEMP: r"$T$, [$^{\circ}$C]",
}

colorbar_ticks: dict[PlotPane, tuple[float, ...]] = {
    PlotPane.MEAN_DOPP_VEL: [-2, -1, 0, 1, 2, 3, 4],
    PlotPane.REFL: [-60, -50, -40, -30, -20, -10, 0, 10, 20, 30],
    PlotPane.SPEC_WIDTH: [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4],
    PlotPane.DEPOL: [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
    PlotPane.TEMP: [-40, -30, -20, -10, 0, 10, 20, 30],
}
