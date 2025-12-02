# Copyright (c) 2025 Will Zhang
# License MIT License
# pyright: reportUnknownMemberType=false

import argparse
from functools import reduce
from operator import iand
from pathlib import Path
from typing import TYPE_CHECKING, Literal, NamedTuple, TypedDict, Unpack

import numpy as np
from pytools.result import Err, Ok
from taad_smc.io.api import import_df

from ._plotting import plotxy, semilogx
from ._types import PlotData

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    import pandas as pd
    from pytools.plotting.trait import PlotKwargs

parser = argparse.ArgumentParser(
    description="Read a TDMS file and print its contents.",
)
parser.add_argument("file", type=str, nargs="+", help="Path to the TDMS file to read.")


class Arguments(TypedDict):
    """TypedDict for command line arguments."""

    file: Sequence[Path]


def parse_args(args: list[str] | None = None) -> Arguments:
    files = [v for f in parser.parse_args(args).file for v in Path().glob(f)]
    return {"file": files}


def filter_df(data: pd.DataFrame, terms: Sequence[str]) -> pd.DataFrame:
    filters = [data["protocol"].str.contains(t, case=False) for t in terms]
    merged_filter: pd.Series[bool] = reduce(iand, filters)
    return data[merged_filter]


def make_semilogplot(
    data: pd.DataFrame,
    terms: Sequence[str],
    file: Path,
    **kwargs: Unpack[PlotKwargs],
) -> Ok[None] | Err:
    filtered_data = filter_df(data, terms)
    if filtered_data.empty:
        msg = f"No data found with terms: {terms}"
        return Err(LookupError(msg))
    segmented_data = [x for _, x in filtered_data.groupby("protocol", sort=False)]
    plot_data: Sequence[PlotData[np.float64]] = [
        PlotData(
            p["time"].to_numpy(np.float64) - p["time"].to_numpy(np.float64).min(),
            p["force"].to_numpy(np.float64),
        )
        for p in segmented_data
    ]
    kwargs["xlabel"] = "Time (s)"
    kwargs["ylabel"] = "Force (mN)"
    kwargs["curve_labels"] = [p["protocol"].iloc[0] for p in segmented_data]
    kwargs["padbottom"] = 0.15
    semilogx(
        plot_data,
        file.parent / f"Post_{'_'.join(terms)}_plot.png",
        **kwargs,
    )
    return Ok(None)


def make_plotxy(
    data: pd.DataFrame,
    terms: Sequence[str],
    file: Path,
    **kwargs: Unpack[PlotKwargs],
) -> Ok[None] | Err:
    filtered_data = filter_df(data, terms)
    if filtered_data.empty:
        msg = f"No data found with terms: {terms}"
        return Err(LookupError(msg))
    cycle = filtered_data["cycle"] == "cycle_2"
    filtered_data = filtered_data[cycle]
    segmented_data = [x for _, x in filtered_data.groupby("protocol", sort=False)]
    plot_data = [
        PlotData(
            p["disp"].to_numpy(np.float64),
            p["force"].to_numpy(np.float64),
        )
        for p in segmented_data
    ]
    kwargs["xlabel"] = "Strain"
    kwargs["ylabel"] = "Force (mN)"
    kwargs["curve_labels"] = [p["protocol"].iloc[0] for p in segmented_data]
    kwargs["padbottom"] = 0.15
    plotxy(
        plot_data,
        file.parent / f"Post_{'_'.join(terms)}_plot.png",
        **kwargs,
    )
    return Ok(None)


def make_plottime(
    data: pd.DataFrame,
    terms: Sequence[str],
    file: Path,
    **kwargs: Unpack[PlotKwargs],
) -> Ok[None] | Err:
    filtered_data = filter_df(data, terms)
    if filtered_data.empty:
        return Err(LookupError(f"No data found with terms: {terms}"))
    segmented_data = [x for _, x in filtered_data.groupby("protocol", sort=False)]
    plot_data = [
        PlotData(
            p["time"].to_numpy(np.float64),
            p["force"].to_numpy(np.float64),
        )
        for p in segmented_data
    ]
    kwargs["xlabel"] = "Time (s)"
    kwargs["ylabel"] = "Force (mN)"
    kwargs["curve_labels"] = [p["protocol"].iloc[0] for p in segmented_data]
    kwargs["padbottom"] = 0.15
    plotxy(
        plot_data,
        file.parent / f"Post_{'_'.join(terms)}_plot.png",
        **kwargs,
    )
    return Ok(None)


def make_plot(
    data: pd.DataFrame,
    terms: Sequence[str],
    file: Path,
    mode: Literal["xy", "semilog", "time"],
    **kwargs: Unpack[PlotKwargs],
) -> Ok[None] | Err:
    match mode:
        case "xy":
            return make_plotxy(data, terms, file, **kwargs)
        case "semilog":
            return make_semilogplot(data, terms, file, **kwargs)
        case "time":
            return make_plottime(data, terms, file, **kwargs)


class PlotSpec(NamedTuple):
    terms: Sequence[str]
    mode: Literal["xy", "semilog", "time"]


PLOTS: Mapping[str, PlotSpec] = {
    "activation_log": PlotSpec(("Activation",), "semilog"),
    "activation_xy": PlotSpec(("Activation",), "time"),
    "precondition": PlotSpec(("Preconditioning",), "xy"),
    "relaxation": PlotSpec(("Relax",), "semilog"),
    "cycling_30": PlotSpec(("Saw", "30"), "xy"),
    "cycling_20": PlotSpec(("Saw", "20"), "xy"),
    "cycling_10": PlotSpec(("Saw", "10"), "xy"),
    "cycling_slow": PlotSpec(("Saw", "slow"), "xy"),
    "cycling_mid": PlotSpec(("Saw", "mid"), "xy"),
    "cycling_fast": PlotSpec(("Saw", "fast"), "xy"),
}


def main(file: Path) -> None:
    if not file.exists():
        print(f"File {file} does not exist, skipping...")
        return
    data = import_df(file).unwrap()
    ylim = (data["force"].min() - 25, data["force"].max() + 25)
    for spec in PLOTS.values():
        match make_plot(data, spec.terms, file, spec.mode, ylim=ylim):
            case Ok(None):
                print("Plot created successfully.")
            case Err(msg):
                print(f"Plot skipped: {msg}")


if __name__ == "__main__":
    args = parse_args()
    for f in args["file"]:
        main(f)
