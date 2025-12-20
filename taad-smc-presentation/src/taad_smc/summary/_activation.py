"""Summarize activation data."""

from typing import TYPE_CHECKING, Literal, Unpack

import numpy as np
from pytools.plotting.trait import PlotKwargs
from pytools.result import Err, Ok

from ._plotting import semilogx_on_axis
from ._tools import get_last_valid
from ._types import PlotData

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    import pandas as pd
    from matplotlib.axes import Axes
    from pytools.logging.trait import ILogger
    from taad_smc.io.api import SpecimenData


def parse_activation_data(
    database: SpecimenData,
) -> Ok[Mapping[Literal["activation", "deactivation", "initial"], pd.DataFrame]] | Err:
    match get_last_valid(database, "initial"):
        case Err(e):
            return Err(e)
        case Ok(initial_data):
            pass
    match get_last_valid(database, "activation"):
        case Err(e):
            return Err(e)
        case Ok(activation_data):
            pass
    match get_last_valid(database, "deactivation"):
        case Err(e):
            return Err(e)
        case Ok(deactivation_data):
            pass
    data: Mapping[Literal["activation", "deactivation", "initial"], pd.DataFrame | None] = {
        "activation": activation_data,
        "deactivation": deactivation_data,
        "initial": initial_data,
    }
    data = {k: v[v["protocol"] == "Relax_Mid"] for k, v in data.items() if v is not None}
    return Ok(data)


def _create_plot_data_i(
    data: pd.DataFrame,
) -> PlotData[np.float64]:
    idx = data[data["mode"] == "HOLD"].index[0]
    time = data["time"] - data["time"].loc[idx] + 25.0
    time = time.to_numpy(dtype=np.float64)
    return PlotData(
        x=time,
        y=data[["force"]].to_numpy(dtype=np.float64).flatten(),
    )


def _create_plot_data(
    data: Mapping[Literal["activation", "deactivation", "initial"], pd.DataFrame],
) -> Mapping[str, PlotData[np.float64]]:
    return {k: _create_plot_data_i(df) for k, df in data.items()}


def summarize_activation_data(
    plot_grid: Sequence[Sequence[Axes]],
    database: SpecimenData,
    *,
    log: ILogger,
    **kwargs: Unpack[PlotKwargs],
) -> Ok[None] | Err:
    match parse_activation_data(database):
        case Ok(data):
            if not data:
                log.info("No activation-related data found. Skipping ...")
                return Ok(None)
        case Err(e):
            return Err(e)
    activation_colors = {
        "initial": "k",
        "activation": "r",
        "deactivation": "b",
    }
    plot_data = _create_plot_data(data)
    plot_kwargs = (
        PlotKwargs(
            title="Activation Summary",
            xlabel="Time [s]",
            ylabel="Force [mN]",
            color=[activation_colors[k] for k in plot_data],
        )
        | kwargs
    )
    semilogx_on_axis(
        plot_data.values(),
        ax=plot_grid[2][0],
        **plot_kwargs,
    )
    return Ok(None)
