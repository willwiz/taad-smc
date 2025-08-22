# Copyright (c) 2025 Will Zhang
# License MIT License
# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
# pyright: reportUnknownMemberType=false

import argparse
from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING, TypedDict, cast

import numpy as np

from taad_smc.io.api import import_data
from taad_smc.plotting.semilog import plotxy, semilogx
from taad_smc.plotting.struct import PlotData

if TYPE_CHECKING:
    import pandas as pd

parser = argparse.ArgumentParser(
    description="Read a TDMS file and print its contents.",
)
parser.add_argument("file", type=str, nargs="+", help="Path to the TDMS file to read.")


class Arguments(TypedDict):
    """TypedDict for command line arguments."""

    file: Sequence[Path]


def parse_args(args: list[str] | None = None) -> Arguments:
    """Return parsed command line arguments as a dataclass.

    Parameters
    ----------
    args : list[str] | None, optional
        Command line arguments, by default None

    Returns
    -------
    Arguments
        Parsed command line arguments as a dataclass.

    """
    files = [v for f in parser.parse_args(args).file for v in Path().glob(f)]
    return {"file": files}


def main(file: Path) -> None:
    data = import_data(file)
    relaxation_data = data[data["protocol"].str.contains("relax", case=False)]
    segmented_data = cast(
        "Sequence[pd.DataFrame]",
        [x for _, x in relaxation_data.groupby("protocol", sort=False)],
    )
    plot_data = [
        PlotData(
            p["time"].to_numpy(np.float64) - p["time"].to_numpy(np.float64).min(),
            p["force"].to_numpy(np.float64),
        )
        for p in segmented_data
    ]
    semilogx(
        plot_data,
        file.parent / "Post_relaxation_plot.png",
        xlabel="Time (s)",
        ylabel="Force (mN)",
        curve_labels=[p["protocol"].iloc[0] for p in segmented_data],
        padbottom=0.2,
    )
    unique_15_data = data[data["protocol"].str.contains("15", case=False)]
    segmented_data = cast(
        "Sequence[pd.DataFrame]",
        [x for _, x in unique_15_data.groupby("protocol", sort=False)],
    )
    plot_data = [
        PlotData(
            p["disp"].to_numpy(np.float64),
            p["force"].to_numpy(np.float64),
        )
        for p in segmented_data
    ]
    plotxy(
        plot_data,
        file.parent / ("Post_unique_15_plot.png"),
        xlabel="Strain",
        ylabel="Force (mN)",
        curve_labels=[p["protocol"].iloc[0] for p in segmented_data],
        padbottom=0.2,
    )
    unique_10_data = data[data["protocol"].str.contains("10", case=False)]
    segmented_data = cast(
        "Sequence[pd.DataFrame]",
        [x for _, x in unique_10_data.groupby("protocol", sort=False)],
    )
    plot_data = [
        PlotData(
            p["disp"].to_numpy(np.float64),
            p["force"].to_numpy(np.float64),
        )
        for p in segmented_data
    ]
    plotxy(
        plot_data,
        file.parent / ("Post_unique_10_plot.png"),
        xlabel="Strain",
        ylabel="Force (mN)",
        curve_labels=[p["protocol"].iloc[0] for p in segmented_data],
        padbottom=0.2,
    )
    unique_5_data = data[data["protocol"].str.contains("_5", case=False)]
    segmented_data = cast(
        "Sequence[pd.DataFrame]",
        [x for _, x in unique_5_data.groupby("protocol", sort=False)],
    )
    print(segmented_data)
    plot_data = [
        PlotData(
            p["disp"].to_numpy(np.float64),
            p["force"].to_numpy(np.float64),
        )
        for p in segmented_data
    ]
    plotxy(
        plot_data,
        file.parent / ("Post_unique_5_plot.png"),
        xlabel="Strain",
        ylabel="Force (mN)",
        curve_labels=[p["protocol"].iloc[0] for p in segmented_data],
        padbottom=0.2,
    )
    unique_fast_data = data[
        data["protocol"].str.contains("Saw", case=False)
        & data["protocol"].str.contains("fast", case=False)
    ]
    segmented_data = cast(
        "Sequence[pd.DataFrame]",
        [x for _, x in unique_fast_data.groupby("protocol", sort=False)],
    )
    plot_data = [
        PlotData(
            p["disp"].to_numpy(np.float64),
            p["force"].to_numpy(np.float64),
        )
        for p in segmented_data
    ]
    plotxy(
        plot_data,
        file.parent / ("Post_unique_fast_plot.png"),
        xlabel="Strain",
        ylabel="Force (mN)",
        curve_labels=[p["protocol"].iloc[0] for p in segmented_data],
        padbottom=0.2,
    )
    unique_mid_data = data[
        data["protocol"].str.contains("Saw", case=False)
        & data["protocol"].str.contains("mid", case=False)
    ]
    segmented_data = cast(
        "Sequence[pd.DataFrame]",
        [x for _, x in unique_mid_data.groupby("protocol", sort=False)],
    )
    plot_data = [
        PlotData(
            p["disp"].to_numpy(np.float64),
            p["force"].to_numpy(np.float64),
        )
        for p in segmented_data
    ]
    plotxy(
        plot_data,
        file.parent / ("Post_unique_mid_plot.png"),
        xlabel="Strain",
        ylabel="Force (mN)",
        curve_labels=[p["protocol"].iloc[0] for p in segmented_data],
        padbottom=0.2,
    )
    unique_slow_data = data[
        data["protocol"].str.contains("Saw", case=False)
        & data["protocol"].str.contains("slow", case=False)
    ]
    segmented_data = cast(
        "Sequence[pd.DataFrame]",
        [x for _, x in unique_slow_data.groupby("protocol", sort=False)],
    )
    plot_data = [
        PlotData(
            p["disp"].to_numpy(np.float64),
            p["force"].to_numpy(np.float64),
        )
        for p in segmented_data
    ]
    plotxy(
        plot_data,
        file.parent / ("Post_unique_slow_plot.png"),
        xlabel="Strain",
        ylabel="Force (mN)",
        curve_labels=[p["protocol"].iloc[0] for p in segmented_data],
        padbottom=0.2,
    )


if __name__ == "__main__":
    args = parse_args()
    for f in args["file"]:
        main(f)
