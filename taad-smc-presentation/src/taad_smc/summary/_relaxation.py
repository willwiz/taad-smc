"""Summarize activation data."""

from functools import reduce
from operator import iand
from typing import TYPE_CHECKING, Literal, Unpack

import numpy as np
from pytools.plotting.trait import PlotKwargs
from pytools.result import Err, Ok

from ._plotting import semilogx_on_axis
from ._tools import get_last_valid
from ._types import PlotData

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping, Sequence

    import pandas as pd
    from matplotlib.axes import Axes
    from pytools.logging.trait import ILogger
    from taad_smc.io.api import SpecimenData


def reduce_relaxation_terms(df: pd.DataFrame, terms: Iterable[str]) -> pd.DataFrame:
    filters = [df["protocol"].str.contains(t, case=False) for t in terms]
    merged_filter: pd.Series[bool] = reduce(iand, filters)
    return df[merged_filter]


def parse_relaxation_data(
    database: SpecimenData,
) -> (
    Ok[
        Mapping[
            Literal["Fast", "Mid", "Slow"],
            Mapping[Literal["activated", "deactivated", "initial"], pd.DataFrame],
        ]
    ]
    | Err
):
    match get_last_valid(database, "initial"):
        case Err(e):
            return Err(e)
        case Ok(initial_data):
            pass
    match get_last_valid(database, "activated"):
        case Err(e):
            return Err(e)
        case Ok(activation_data):
            pass
    match get_last_valid(database, "deactivated"):
        case Err(e):
            return Err(e)
        case Ok(deactivation_data):
            pass
    data: Mapping[Literal["activated", "deactivated", "initial"], pd.DataFrame | None] = {
        "activated": activation_data,
        "deactivated": deactivation_data,
        "initial": initial_data,
    }
    filtered_data: Mapping[
        Literal["Fast", "Mid", "Slow"],
        Mapping[Literal["activated", "deactivated", "initial"], pd.DataFrame],
    ] = {
        s: {k: reduce_relaxation_terms(v, ("Relax", s)) for k, v in data.items() if v is not None}
        for s in ("Fast", "Mid", "Slow")
    }
    return Ok(filtered_data)


def convert_plot_data_time(
    data: pd.DataFrame,
) -> PlotData[np.float64]:
    time = data[["time"]].to_numpy(dtype=np.float64).flatten()
    time = time - time.min()
    return PlotData(
        x=time,
        y=data[["force"]].to_numpy(dtype=np.float64).flatten(),
    )


def _create_plot_data(
    data: Mapping[
        Literal["Fast", "Mid", "Slow"],
        Mapping[Literal["activated", "deactivated", "initial"], pd.DataFrame],
    ],
) -> Mapping[str, Mapping[str, PlotData[np.float64]]]:
    return {k: {s: convert_plot_data_time(df) for s, df in v.items()} for k, v in data.items()}


def summarize_relaxation_data(
    plot_grid: Sequence[Sequence[Axes]],
    database: SpecimenData,
    *,
    log: ILogger,
    **kwargs: Unpack[PlotKwargs],
) -> Ok[None] | Err:
    match parse_relaxation_data(database):
        case Ok(data):
            if not data:
                log.info("No relaxation-related data found. Skipping ...")
                return Ok(None)
        case Err(e):
            return Err(e)
    activation_colors = {
        "initial": "k",
        "activated": "r",
        "deactivated": "b",
    }
    lin_sty = {"Fast": "-", "Mid": "--", "Slow": ":"}
    plot_data = _create_plot_data(data)
    for i, (s, v) in enumerate(plot_data.items()):
        plot_kwargs = (
            PlotKwargs(
                title=f"Relaxation w/ activation - {s}",
                xlabel="Time [s]",
                ylabel="Force [mN]",
                color=[activation_colors[k] for k in v],
                linestyle=lin_sty[s],
            )
            | kwargs
        )
        semilogx_on_axis(v.values(), ax=plot_grid[2][i + 1], **plot_kwargs)
    return Ok(None)
