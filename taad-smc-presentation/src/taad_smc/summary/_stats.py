"""Summarize activation data."""

from functools import reduce
from operator import iand
from typing import TYPE_CHECKING, Literal, Unpack

from pytools.plotting.trait import PlotKwargs
from pytools.result import Err, Ok

from ._plotting import grouped_bar_on_axis
from ._tools import get_last_valid

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


def parse_peak_force_data(
    database: SpecimenData,
) -> Ok[Mapping[str, Mapping[str, float]]] | Err:
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
        "initial": initial_data,
        "activated": activation_data,
        "deactivated": deactivation_data,
    }
    filtered_data: Mapping[str, Mapping[str, float]] = {
        s: {
            k: reduce_cycling_terms(v, ("Saw", "30", s))["force"].max()
            for k, v in data.items()
            if v is not None
        }
        for s in ("Fast", "Mid", "Slow")
    }
    return Ok(filtered_data)


def summarize_peak_data(
    plot_grid: Sequence[Sequence[Axes]],
    database: SpecimenData,
    *,
    log: ILogger,
    **kwargs: Unpack[PlotKwargs],
) -> Ok[None] | Err:
    match parse_peak_force_data(database):
        case Ok(data):
            if not data:
                log.info("No cycling-related data found. Skipping ...")
                return Ok(None)
        case Err(e):
            return Err(e)
    # lin_sty = {"Fast": "-", "Mid": "--", "Slow": ":"}
    rate_hatches = {
        "Slow": ".",
        "Mid": "x",
        "Fast": " ",
    }
    rate_colors = {
        "Slow": "none",
        "Mid": "none",
        "Fast": "grey",
    }
    activation_colors = {
        "initial": "k",
        "activated": "r",
        "deactivated": "b",
    }
    plot_kwargs = (
        PlotKwargs(
            title="Peak Cycling Loading Stress",
            ylabel="Force [mN]",
        )
        | kwargs
    )
    grouped_bar_on_axis(
        data,
        ax=plot_grid[1][0],
        bar_color=activation_colors,
        hatches=rate_hatches,
        fill_color=rate_colors,
        **plot_kwargs,
    )
    return Ok(None)
