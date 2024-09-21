"""Custom plot labels."""

from sio_postdoc.manager import PlotPane

plot_labels: dict[PlotPane, str] = {
    PlotPane.MEAN_DOPP_VEL: r"Radar Mean Doppler Velocity, $V_D$",
    PlotPane.REFL: r"Radar Reflectivity, $Z_e$",
    PlotPane.SPEC_WIDTH: r"Radar Spectral Width, $W_D$",
    PlotPane.DEPOL: r"Lidar Depolarization Ratio, $\delta$",
    PlotPane.LWP: r"Liquid Water Path, $m^{\prime \prime}$",
    PlotPane.DLR: r"Downwelling Longwave Radiation, $\dot{E}_{\ell} \hspace{-0.15}^{\prime \prime}$",
    PlotPane.TEMP: r"Atmospheric Temperature, $T$",
}

plot_ylabels: dict[PlotPane, str] = {
    PlotPane.MEAN_DOPP_VEL: "Height [km, AGL]",
    PlotPane.REFL: "Height [km, AGL]",
    PlotPane.SPEC_WIDTH: "Height [km, AGL]",
    PlotPane.DEPOL: "Height [km, AGL]",
    PlotPane.LWP: r"$m^{\prime \prime}$ [g/m$^2$]",
    PlotPane.DLR: r"$\dot{E}_{\ell} \hspace{-0.15}^{\prime \prime}$ [W/m$^2$]",
    PlotPane.TEMP: "Height [km, AGL]",
}
