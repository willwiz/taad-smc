# Copyright (c) 2025 Will Zhang
# License: MIT License
import argparse
import typing
from pathlib import Path
from typing import TypedDict, Unpack

from pytools.logging.api import BLogger, XLogger
from pytools.logging.trait import LOG_LEVEL
from pytools.result import Err, Ok

from ._nptdms import import_tdms_muscle_typeless
from ._plot import plot_data
from .api import export_tdms

if typing.TYPE_CHECKING:
    from collections.abc import Sequence

parser = argparse.ArgumentParser(
    description="Read a TDMS file and print its contents.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument("file", type=str, nargs="+", help="Path to the TDMS file to read.")
parser.add_argument("--plot", action="store_true", help="Plot the raw data too.")
parser.add_argument("--overwrite", action="store_true", help="Overwrite existing .raw files.")
parser.add_argument(
    "--log",
    type=str,
    default=None,
    choices=typing.get_args(LOG_LEVEL),
    help="Set the logging level. One of DEBUG, INFO, WARNING, ERROR, CRITICAL.",
)


class OptionKwargs(TypedDict):
    plot: bool
    overwrite: bool
    log: LOG_LEVEL | None


class Arguments(TypedDict):
    file: Sequence[Path]
    opts: OptionKwargs


def parse_args(args: list[str] | None = None) -> Arguments:
    files = [v for val in parser.parse_args(args).file for v in Path().glob(val)]
    return {
        "file": files,
        "opts": {
            "plot": parser.parse_args(args).plot,
            "log": parser.parse_args(args).log,
            "overwrite": parser.parse_args(args).overwrite,
        },
    }


def main(file: str | Path, **kwargs: Unpack[OptionKwargs]) -> None:
    file = Path(file)
    if file.with_suffix(".raw").exists() and not kwargs.get("overwrite"):
        return
    log_level = kwargs.get("log")
    log = (
        BLogger("BRIEF") if log_level is None else XLogger(log_level, file.with_suffix(".tdms_log"))
    )
    log.brief(f"Reading TDMS file: {file}")
    match import_tdms_muscle_typeless(file):
        case Ok(data):
            export_tdms(data, prefix=file)
        case Err(e):
            raise e
    if kwargs.get("plot"):
        plot_data(data, fout=file.with_suffix(".png"))
    log.brief("Done.")


if __name__ == "__main__":
    args = parse_args()
    for f in args["file"]:
        main(f, **args["opts"])
