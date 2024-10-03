"""Custom colorbars for visualizations."""

from sio_postdoc.manager import PlotPane

BOTH: str = "both"
MAX: str = "max"
NEITHER: str = "neither"
PHASES_SHUPE_2007: str = "Phase (Shupe, 2007)"
PHASES_SHUPE_2011: str = "Phase (Shupe, 2011)"
PHASE_TICKS_SHUPE_2007: list[int] = [0, 1, 2, 3, 4, 5, 6]
PHASE_TICKS_SHUPE_2011: list[int] = [0, 1, 2, 3, 4, 5, 6]
PHASE_TICK_LABELS_SHUPE_2007: list[int] = [
    "none",
    "snow",
    "ice",
    "mixed",
    "liquid",
    "drizzle",
    "rain",
]
PHASE_TICK_LABELS_SHUPE_2011: list[int] = [
    "none",
    "ice",
    "mixed ice",
    "mixed",
    "mixed liquid",
    "liquid",
    "rain",
]

colorbar_extend: dict[PlotPane, str] = {
    PlotPane.MEAN_DOPP_VEL: BOTH,
    PlotPane.REFL: BOTH,
    PlotPane.SPEC_WIDTH: MAX,
    PlotPane.DEPOL: NEITHER,
    PlotPane.TEMP: BOTH,
    PlotPane.STEP_1: NEITHER,
    PlotPane.STEP_2: NEITHER,
    PlotPane.STEP_3: NEITHER,
    PlotPane.STEP_4A: NEITHER,
    PlotPane.STEP_RADAR_EDGES: NEITHER,
    PlotPane.STEP_LIDAR_EDGES: NEITHER,
    PlotPane.STEP_OCCULTATION_ZONE: NEITHER,
    PlotPane.STEP_4B: NEITHER,
    PlotPane.STEP_5: NEITHER,
    PlotPane.STEP_6: NEITHER,
    PlotPane.STEP_7: NEITHER,
    PlotPane.STEP_8: NEITHER,
    PlotPane.REFERENCE: NEITHER,
    PlotPane.RENUMBERED: NEITHER,
    PlotPane.MODIFIED_MIXED: NEITHER,
}

colorbar_labels: dict[PlotPane, str] = {
    PlotPane.MEAN_DOPP_VEL: r"$V_D$, [m/s] (positive: up)",
    PlotPane.REFL: r"$Z_e$, [dBZ]",
    PlotPane.SPEC_WIDTH: r"$W_D$, [m/s]",
    PlotPane.DEPOL: r"$\delta$",
    PlotPane.TEMP: r"$T$, [$^{\circ}$C]",
    PlotPane.STEP_1: PHASES_SHUPE_2007,
    PlotPane.STEP_2: PHASES_SHUPE_2007,
    PlotPane.STEP_3: PHASES_SHUPE_2007,
    PlotPane.STEP_4A: PHASES_SHUPE_2007,
    PlotPane.STEP_RADAR_EDGES: "Radar Edges",
    PlotPane.STEP_LIDAR_EDGES: "Lidar Edges",
    PlotPane.STEP_OCCULTATION_ZONE: "Occultation Zone",
    PlotPane.STEP_4B: PHASES_SHUPE_2007,
    PlotPane.STEP_5: PHASES_SHUPE_2007,
    PlotPane.STEP_6: PHASES_SHUPE_2007,
    PlotPane.STEP_7: PHASES_SHUPE_2007,
    PlotPane.STEP_8: PHASES_SHUPE_2007,
    PlotPane.REFERENCE: PHASES_SHUPE_2007,
    PlotPane.RENUMBERED: PHASES_SHUPE_2011,
    PlotPane.MODIFIED_MIXED: PHASES_SHUPE_2011,
}

colorbar_ticks: dict[PlotPane, tuple[float, ...]] = {
    PlotPane.MEAN_DOPP_VEL: [-3, -2, -1, 0, 1, 2, 3, 4],
    PlotPane.REFL: [-60, -50, -40, -30, -20, -10, 0, 10, 20, 30],
    PlotPane.SPEC_WIDTH: [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4],
    PlotPane.DEPOL: [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
    PlotPane.TEMP: [-60, -50, -40, -30, -20, -10, 0, 10, 20, 30],
    PlotPane.STEP_1: PHASE_TICKS_SHUPE_2007,
    PlotPane.STEP_2: PHASE_TICKS_SHUPE_2007,
    PlotPane.STEP_3: PHASE_TICKS_SHUPE_2007,
    PlotPane.STEP_4A: PHASE_TICKS_SHUPE_2007,
    PlotPane.STEP_RADAR_EDGES: [-1, 0, 1],
    PlotPane.STEP_LIDAR_EDGES: [-1, 0, 1],
    PlotPane.STEP_OCCULTATION_ZONE: [0, 1],
    PlotPane.STEP_4B: PHASE_TICKS_SHUPE_2007,
    PlotPane.STEP_5: PHASE_TICKS_SHUPE_2007,
    PlotPane.STEP_6: PHASE_TICKS_SHUPE_2007,
    PlotPane.STEP_7: PHASE_TICKS_SHUPE_2007,
    PlotPane.STEP_8: PHASE_TICKS_SHUPE_2007,
    PlotPane.REFERENCE: PHASE_TICKS_SHUPE_2007,
    PlotPane.RENUMBERED: PHASE_TICKS_SHUPE_2011,
    PlotPane.MODIFIED_MIXED: PHASE_TICKS_SHUPE_2011,
}

colorbar_tick_labels: dict[PlotPane, tuple[float, ...] | None] = {
    PlotPane.MEAN_DOPP_VEL: None,
    PlotPane.REFL: None,
    PlotPane.SPEC_WIDTH: None,
    PlotPane.DEPOL: None,
    PlotPane.TEMP: None,
    PlotPane.STEP_1: PHASE_TICK_LABELS_SHUPE_2007,
    PlotPane.STEP_2: PHASE_TICK_LABELS_SHUPE_2007,
    PlotPane.STEP_3: PHASE_TICK_LABELS_SHUPE_2007,
    PlotPane.STEP_4A: PHASE_TICK_LABELS_SHUPE_2007,
    PlotPane.STEP_RADAR_EDGES: ["base", "neither", "top"],
    PlotPane.STEP_LIDAR_EDGES: ["base", "neither", "top"],
    PlotPane.STEP_OCCULTATION_ZONE: ["no-occultation", "occultation"],
    PlotPane.STEP_4B: PHASE_TICK_LABELS_SHUPE_2007,
    PlotPane.STEP_5: PHASE_TICK_LABELS_SHUPE_2007,
    PlotPane.STEP_6: PHASE_TICK_LABELS_SHUPE_2007,
    PlotPane.STEP_7: PHASE_TICK_LABELS_SHUPE_2007,
    PlotPane.STEP_8: PHASE_TICK_LABELS_SHUPE_2007,
    PlotPane.REFERENCE: PHASE_TICK_LABELS_SHUPE_2007,
    PlotPane.RENUMBERED: PHASE_TICK_LABELS_SHUPE_2011,
    PlotPane.MODIFIED_MIXED: PHASE_TICK_LABELS_SHUPE_2011,
}


colorbar_shrinks: dict[PlotPane, float] = {
    PlotPane.MEAN_DOPP_VEL: 1,
    PlotPane.REFL: 1,
    PlotPane.SPEC_WIDTH: 1,
    PlotPane.DEPOL: 1,
    PlotPane.TEMP: 1,
    PlotPane.STEP_1: 1,
    PlotPane.STEP_2: 1,
    PlotPane.STEP_3: 1,
    PlotPane.STEP_4A: 1,
    PlotPane.STEP_RADAR_EDGES: 3 / 7,
    PlotPane.STEP_LIDAR_EDGES: 3 / 7,
    PlotPane.STEP_OCCULTATION_ZONE: 2 / 7,
    PlotPane.STEP_4B: 1,
    PlotPane.STEP_5: 1,
    PlotPane.STEP_6: 1,
    PlotPane.STEP_7: 1,
    PlotPane.STEP_8: 1,
    PlotPane.REFERENCE: 1,
    PlotPane.RENUMBERED: 1,
    PlotPane.MODIFIED_MIXED: 1,
}

colorbar_aspects: dict[PlotPane, int] = {
    PlotPane.MEAN_DOPP_VEL: 7,
    PlotPane.REFL: 7,
    PlotPane.SPEC_WIDTH: 7,
    PlotPane.DEPOL: 7,
    PlotPane.TEMP: 7,
    PlotPane.STEP_1: 7,
    PlotPane.STEP_2: 7,
    PlotPane.STEP_3: 7,
    PlotPane.STEP_4A: 7,
    PlotPane.STEP_RADAR_EDGES: 3,
    PlotPane.STEP_LIDAR_EDGES: 3,
    PlotPane.STEP_OCCULTATION_ZONE: 2,
    PlotPane.STEP_4B: 7,
    PlotPane.STEP_5: 7,
    PlotPane.STEP_6: 7,
    PlotPane.STEP_7: 7,
    PlotPane.STEP_8: 7,
    PlotPane.REFERENCE: 7,
    PlotPane.RENUMBERED: 7,
    PlotPane.MODIFIED_MIXED: 7,
}
