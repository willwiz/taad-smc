"""Summarize activation data."""

from functools import reduce
from operator import iand
from typing import TYPE_CHECKING, Literal, Unpack

import numpy as np
from pytools.plotting.trait import PlotKwargs
from pytools.result import Err, Ok
from taad_smc.summary._relaxation import convert_plot_data_time

from ._plotting import plotxy_on_axis, semilogx_on_axis
from ._tools import get_last_valid
from ._types import PlotData

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping, Sequence

    import pandas as pd
    from matplotlib.axes import Axes
    from pytools.logging.trait import ILogger
    from taad_smc.io.api import SpecimenData


def reduce_cycling_terms(df: pd.DataFrame, terms: Iterable[str]) -> pd.DataFrame:
    filters = [df["protocol"].str.contains(t, case=False) for t in terms]
    merged_filter: pd.Series[bool] = reduce(iand, filters)
    idf = df[merged_filter]
    last_cycle: pd.Series[bool] = idf["cycle"] == idf["cycle"].max()
    return idf[last_cycle]


def parse_activated_cycling_data(
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
        s: {k: reduce_cycling_terms(v, ("Saw", "30", s)) for k, v in data.items() if v is not None}
        for s in ("Fast", "Mid", "Slow")
    }
    return Ok(filtered_data)


def parse_cycling_data(
    database: SpecimenData,
) -> (
    Ok[
        Mapping[
            Literal["Fast", "Mid", "Slow"],
            Mapping[Literal["10", "20", "30"], pd.DataFrame],
        ]
    ]
    | Err
):
    match get_last_valid(database, "initial"):
        case Err(e):
            return Err(e)
        case Ok(initial_data):
            pass
    if initial_data is None:
        return Err(LookupError("No initial data found in database."))

    filtered_data: Mapping[
        Literal["Fast", "Mid", "Slow"],
        Mapping[Literal["10", "20", "30"], pd.DataFrame],
    ] = {
        s: {r: reduce_cycling_terms(initial_data, ("Saw", r, s)) for r in ("30", "20", "10")}
        for s in ("Fast", "Mid", "Slow")
    }
    return Ok(filtered_data)


def parse_relaxation_data(
    database: SpecimenData,
) -> (
    Ok[
        Mapping[
            Literal["Fast", "Mid", "Slow"],
            pd.DataFrame,
        ]
    ]
    | Err
):
    match get_last_valid(database, "initial"):
        case Err(e):
            return Err(e)
        case Ok(initial_data):
            pass
    if initial_data is None:
        return Err(LookupError("No initial data found in database."))

    filtered_data: Mapping[
        Literal["Fast", "Mid", "Slow"],
        pd.DataFrame,
    ] = {s: reduce_cycling_terms(initial_data, ("Relax", s)) for s in ("Fast", "Mid", "Slow")}
    return Ok(filtered_data)


def _create_plot_data_i(
    data: pd.DataFrame,
) -> PlotData[np.float64]:
    return PlotData(
        x=data[["disp"]].to_numpy(dtype=np.float64).flatten(),
        y=data[["force"]].to_numpy(dtype=np.float64).flatten(),
    )


def _create_plot_data(
    data: Mapping[
        Literal["Fast", "Mid", "Slow"],
        Mapping[Literal["activated", "deactivated", "initial"], pd.DataFrame],
    ],
) -> Mapping[str, Mapping[str, PlotData[np.float64]]]:
    return {k: {s: _create_plot_data_i(df) for s, df in v.items()} for k, v in data.items()}


def summarize_activated_cycling_data(
    plot_grid: Sequence[Sequence[Axes]],
    database: SpecimenData,
    *,
    log: ILogger,
    **kwargs: Unpack[PlotKwargs],
) -> Ok[None] | Err:
    match parse_activated_cycling_data(database):
        case Ok(data):
            if not data:
                log.info("No cycling-related data found. Skipping ...")
                return Ok(None)
        case Err(e):
            return Err(e)
    plot_data = _create_plot_data(data)
    lin_sty = {"Fast": "-", "Mid": "--", "Slow": ":"}
    activation_colors = {
        "initial": "k",
        "activated": "r",
        "deactivated": "b",
    }
    for i, (s, v) in enumerate(plot_data.items()):
        plot_kwargs = (
            PlotKwargs(
                title=f"Cycling w/ activation - {s}",
                xlabel="Strain [-]",
                ylabel="Force [mN]",
                color=[activation_colors[k] for k in v],
                linestyle=lin_sty[s],
            )
            | kwargs
        )
        plotxy_on_axis(
            v.values(),
            ax=plot_grid[1][i + 1],
            **plot_kwargs,
        )
    return Ok(None)


def _convert_to_plot_data(
    data: Iterable[pd.DataFrame],
) -> Iterable[PlotData[np.float64]]:
    return [
        PlotData(
            x=df[["disp"]].to_numpy(dtype=np.float64).flatten(),
            y=df[["force"]].to_numpy(dtype=np.float64).flatten(),
        )
        for df in data
    ]


def summarize_cycling_data(
    plot_grid: Sequence[Sequence[Axes]],
    database: SpecimenData,
    *,
    log: ILogger,
    **kwargs: Unpack[PlotKwargs],
) -> Ok[None] | Err:
    match parse_cycling_data(database):
        case Ok(data):
            if not data:
                log.info("No cycling-related data found. Skipping ...")
                return Ok(None)
        case Err(e):
            return Err(e)
    strain_colors = {"30": "k", "20": "g", "10": "orange"}
    rate_sty = {"Fast": "-", "Mid": "--", "Slow": ":"}
    plot_kwargs = (
        PlotKwargs(
            title="Cycling - Strain Level",
            xlabel="Strain [-]",
            ylabel="Force [mN]",
            color=[strain_colors[k] for k in data["Fast"]],
        )
        | kwargs
    )
    plotxy_on_axis(
        _convert_to_plot_data(data["Fast"].values()),
        ax=plot_grid[0][1],
        **plot_kwargs,
    )
    plot_kwargs = (
        PlotKwargs(
            title="Cycling - Rate Dependence",
            xlabel="Strain [-]",
            ylabel="Force [mN]",
            color="k",
            linestyle=[rate_sty[k] for k in ("Fast", "Mid", "Slow")],
        )
        | kwargs
    )
    plotxy_on_axis(
        _convert_to_plot_data([data[k]["30"] for k in ("Fast", "Mid", "Slow")]),
        ax=plot_grid[0][2],
        **plot_kwargs,
    )
    match parse_relaxation_data(database):
        case Ok(data):
            if not data:
                log.info("No relaxation-related data found. Skipping ...")
                return Ok(None)
        case Err(e):
            return Err(e)
    plot_kwargs = (
        PlotKwargs(
            title="Relaxation",
            xlabel="Time [s]",
            ylabel="Force [mN]",
            color="k",
            linestyle=["-", "--", ":"],
        )
        | kwargs
    )
    semilogx_on_axis(
        (convert_plot_data_time(data[k]) for k in ("Fast", "Mid", "Slow")),
        ax=plot_grid[0][3],
        **plot_kwargs,
    )
    return Ok(None)
