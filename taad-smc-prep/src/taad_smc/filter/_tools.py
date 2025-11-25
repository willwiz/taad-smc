# pyright: reportUnknownMemberType=false
from functools import reduce
from operator import iand
from typing import TYPE_CHECKING, Literal, NamedTuple, TypedDict, Unpack

import numpy as np
import pandas as pd
from pytools.plotting.trait import PlotKwargs
from pytools.result import Err, Ok

from ._plotting import plotxy, semilogx
from .types import PlotData

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence
    from pathlib import Path


def find_split_points(df: pd.DataFrame, headers: Sequence[str]) -> pd.Index:
    last_points = df[headers].drop_duplicates(keep="last").index
    return pd.Index(np.concatenate([[0], last_points + 1]))


def filter_df(data: pd.DataFrame, terms: Sequence[str]) -> pd.Series[bool]:
    filters = [data["protocol"].str.contains(t, case=False) for t in terms]
    merged_filter: pd.Series[bool] = reduce(iand, filters)
    return merged_filter


def make_semilogplot(
    df: pd.DataFrame,
    ff: pd.DataFrame,
    terms: Sequence[str],
    file: Path,
    **kwargs: Unpack[PlotKwargs],
) -> Ok[None] | Err:
    mask = filter_df(df, terms)
    if not mask.any():
        msg = f"No data found with terms: {terms}"
        return Err(LookupError(msg))
    df_data = [x for _, x in df[mask].groupby("protocol", sort=False)]
    ff_data = [x for _, x in ff[mask].groupby("protocol", sort=False)]
    plot_data: Sequence[PlotData[np.float64]] = [
        PlotData(
            p["time"].to_numpy(np.float64) - p["time"].to_numpy(np.float64).min(),
            p["force"].to_numpy(np.float64),
        )
        for p in df_data
    ] + [
        PlotData(
            p["time"].to_numpy(np.float64) - p["time"].to_numpy(np.float64).min(),
            p["force"].to_numpy(np.float64),
        )
        for p in ff_data
    ]
    kwargs["xlabel"] = "Time (s)"
    kwargs["ylabel"] = "Force (mN)"
    kwargs["curve_labels"] = [p["protocol"].iloc[0] for p in df_data]
    kwargs["padbottom"] = 0.15
    kwargs["color"] = ["r", "orange", "g", "b", "c", "m", "y"][: len(df_data)] * 2
    kwargs["alpha"] = [0.3] * len(df_data) + [1.0] * len(ff_data)
    semilogx(
        plot_data,
        file.parent / f"{file.stem}_{'_'.join(terms)}_plot.{file.suffix}",
        **kwargs,
    )
    return Ok(None)


def make_plotxy(
    df: pd.DataFrame,
    ff: pd.DataFrame,
    terms: Sequence[str],
    file: Path,
    **kwargs: Unpack[PlotKwargs],
) -> Ok[None] | Err:
    mask = filter_df(df, terms)
    if not mask.any():
        msg = f"No data found with terms: {terms}"
        return Err(LookupError(msg))
    df_data = [x for _, x in df[mask].groupby("protocol", sort=False)]
    ff_data = [x for _, x in ff[mask].groupby("protocol", sort=False)]
    plot_data: Sequence[PlotData[np.float64]] = [
        PlotData(p["disp"].to_numpy(np.float64), p["force"].to_numpy(np.float64)) for p in df_data
    ] + [PlotData(p["disp"].to_numpy(np.float64), p["force"].to_numpy(np.float64)) for p in ff_data]
    kwargs["xlabel"] = "Strain"
    kwargs["ylabel"] = "Force (mN)"
    kwargs["curve_labels"] = [p["protocol"].iloc[0] for p in df_data]
    kwargs["padbottom"] = 0.15
    kwargs["color"] = ["r", "orange", "g", "b", "c", "m", "y"][: len(df_data)] * 2
    kwargs["alpha"] = [0.3] * len(df_data) + [1.0] * len(ff_data)
    plotxy(
        plot_data,
        file.parent / f"{file.stem}_{'_'.join(terms)}_plot.{file.suffix}",
        **kwargs,
    )
    return Ok(None)


def make_plottime(
    df: pd.DataFrame,
    ff: pd.DataFrame,
    terms: Sequence[str],
    file: Path,
    **kwargs: Unpack[PlotKwargs],
) -> Ok[None] | Err:
    mask = filter_df(df, terms)
    if not mask.any():
        return Err(LookupError(f"No data found with terms: {terms}"))
    df_data = [x for _, x in df[mask].groupby("protocol", sort=False)]
    ff_data = [x for _, x in ff[mask].groupby("protocol", sort=False)]
    plot_data: Sequence[PlotData[np.float64]] = [
        PlotData(
            p["time"].to_numpy(np.float64) - p["time"].to_numpy(np.float64).min(),
            p["force"].to_numpy(np.float64),
        )
        for p in df_data
    ] + [
        PlotData(
            p["time"].to_numpy(np.float64) - p["time"].to_numpy(np.float64).min(),
            p["force"].to_numpy(np.float64),
        )
        for p in ff_data
    ]
    kwargs["xlabel"] = "Time (s)"
    kwargs["ylabel"] = "Force (mN)"
    kwargs["curve_labels"] = [p["protocol"].iloc[0] for p in df_data]
    kwargs["padbottom"] = 0.15
    kwargs["color"] = ["r", "orange", "g", "b", "c", "m", "y"][: len(df_data)] * 2
    kwargs["alpha"] = [0.3] * len(df_data) + [1.0] * len(ff_data)
    plotxy(
        plot_data,
        file.parent / f"{file.stem}_{'_'.join(terms)}_plot.{file.suffix}",
        **kwargs,
    )
    return Ok(None)


def make_plot(
    df: pd.DataFrame,
    ff: pd.DataFrame,
    terms: Sequence[str],
    file: Path,
    mode: Literal["xy", "semilog", "time"],
    **kwargs: Unpack[PlotKwargs],
) -> Ok[None] | Err:
    match mode:
        case "xy":
            return make_plotxy(df, ff, terms, file, **kwargs)
        case "semilog":
            return make_semilogplot(df, ff, terms, file, **kwargs)
        case "time":
            return make_plottime(df, ff, terms, file, **kwargs)


class PlotLoopKwargs(TypedDict, total=False):
    xlim: tuple[float, float]
    ylim: tuple[float, float]


class PlotSpec(NamedTuple):
    terms: Sequence[str]
    mode: Literal["xy", "semilog", "time"]


PLOTS: Mapping[str, PlotSpec] = {
    "activation_log": PlotSpec(("Activation",), "semilog"),
    "activation_xy": PlotSpec(("Activation",), "time"),
    "precondition": PlotSpec(("Preconditioning",), "time"),
    "relaxation": PlotSpec(("Relax",), "time"),
    "cycling_30": PlotSpec(("Saw", "30"), "time"),
    "cycling_20": PlotSpec(("Saw", "20"), "time"),
    "cycling_10": PlotSpec(("Saw", "10"), "time"),
    "cycling_slow": PlotSpec(("Saw", "slow"), "time"),
    "cycling_mid": PlotSpec(("Saw", "mid"), "time"),
    "cycling_fast": PlotSpec(("Saw", "fast"), "time"),
}


def plot_loop(df: pd.DataFrame, ff: pd.DataFrame, *, fout: Path) -> Ok[None] | Err:
    # ylim = (df["force"].min() - 23, df["force"].max() + 23)
    kwargs = PlotKwargs(linewidth=0.5, figsize=(8, 3), padleft=0.06, dpi=300)
    for spec in PLOTS.values():
        match make_plot(df, ff, spec.terms, fout, spec.mode, **kwargs):
            case Ok():
                print("Plot created successfully.")
            case Err(e):
                print(f"Plot skipped: {e}")
    return Ok(None)
