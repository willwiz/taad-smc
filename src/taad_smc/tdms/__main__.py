# Copyright (c) 2025 Will Zhang
# License: MIT License
import argparse
from collections.abc import Sequence
from pathlib import Path
from typing import TypedDict, Unpack

from ._plot import plot_data
from .api import export_tdms, import_tdms_raw

parser = argparse.ArgumentParser(
    description="Read a TDMS file and print its contents.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument("file", type=str, nargs="+", help="Path to the TDMS file to read.")
parser.add_argument("--plot", action="store_true", help="Plot the raw data too.")


class OptionKwargs(TypedDict):
    plot: bool


class Arguments(TypedDict):
    file: Sequence[Path]
    opts: OptionKwargs


def parse_args(args: list[str] | None = None) -> Arguments:
    files = [v for val in parser.parse_args(args).file for v in Path().glob(val)]
    return {"file": files, "opts": {"plot": parser.parse_args(args).plot}}


def main(file: str | Path, **kwargs: Unpack[OptionKwargs]) -> None:
    file = Path(file)
    data = import_tdms_raw(file)
    export_tdms(data, file)
    if kwargs.get("plot"):
        plot_data(data, fout=file.with_suffix(".png"))


if __name__ == "__main__":
    args = parse_args()
    for f in args["file"]:
        main(f, **args["opts"])
