# Copyright (c) 2025 Will Zhang
# License MIT License
# pyright: reportUnknownMemberType=false

import argparse
import inspect
import types
from functools import reduce
from operator import iand
from pathlib import Path
from typing import TYPE_CHECKING, Literal, NamedTuple, TypedDict, Unpack

import numpy as np
from matplotlib.pylab import Any
from taad_smc.io.api import import_data

from .semilog import plotxy, semilogx
from .struct import PlotData

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


class Okay[T: Any]:
    value: T

    def __init__(self, value: T) -> None:
        self.value = value


class Err:
    value: Exception

    def __init__(self, value: Exception) -> None:
        match inspect.currentframe():
            case None:
                msg = "Failed to get current frame for Err."
                raise RuntimeError(msg)
            case types.FrameType(f_back=frame):
                if frame is None:
                    msg = "Failed to get caller frame for Err."
                    raise RuntimeError(msg)
                tb = types.TracebackType(value.__traceback__, frame, frame.f_lasti, frame.f_lineno)
        self.value = value.with_traceback(tb)


class Success:
    success: bool
    msg: str

    def __init__(self, msg: str) -> None:
        self.success = True
        self.msg = msg


class Failure:
    success: bool
    msg: str

    def __init__(self, msg: str) -> None:
        self.success = False
        self.msg = msg


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
) -> Okay[str] | Failure:
    filtered_data = filter_df(data, terms)
    if filtered_data.empty:
        return Failure(f"No data found with terms: {terms}")
    segmented_data = [x for _, x in filtered_data.groupby("protocol", sort=False)]
    plot_data = [
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
    return Okay(f"Plot <Post_{'_'.join(terms)}_plot.png> created successfully.")


def make_plotxy(
    data: pd.DataFrame,
    terms: Sequence[str],
    file: Path,
    **kwargs: Unpack[PlotKwargs],
) -> Okay[str] | Failure:
    filtered_data = filter_df(data, terms)
    if filtered_data.empty:
        return Failure(f"No data found with terms: {terms}")
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
    return Okay(f"Plot <Post_{'_'.join(terms)}_plot.png> created successfully.")


def make_plottime(
    data: pd.DataFrame,
    terms: Sequence[str],
    file: Path,
    **kwargs: Unpack[PlotKwargs],
) -> Okay[str] | Failure:
    filtered_data = filter_df(data, terms)
    if filtered_data.empty:
        return Failure(f"No data found with terms: {terms}")
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
    return Okay(f"Plot <Post_{'_'.join(terms)}_plot.png> created successfully.")


def make_plot(
    data: pd.DataFrame,
    terms: Sequence[str],
    file: Path,
    mode: Literal["xy", "semilog", "time"],
    **kwargs: Unpack[PlotKwargs],
) -> Okay[str] | Failure:
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
    # "activation_log": PlotSpec(("Activation",), "semilog"),
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
    data = import_data(file)
    ylim = (data["force"].min() - 25, data["force"].max() + 25)
    for spec in PLOTS.values():
        result = make_plot(data, spec.terms, file, spec.mode, ylim=ylim)
        match result:
            case Okay(value=msg):
                print(f"Plot created: {msg}")
            case Failure(msg=msg):
                print(f"Plot skipped: {msg}")


if __name__ == "__main__":
    args = parse_args()
    for f in args["file"]:
        main(f)
