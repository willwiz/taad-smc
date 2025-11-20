import argparse
import dataclasses as dc
from typing import get_args

from pytools.logging.trait import LOG_LEVEL

__all__ = ["parser_cmdline_args"]

_parser = argparse.ArgumentParser(
    description="Split PWL data for taad.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
_parser.add_argument("files", type=str, nargs="+", help="Path to the TDMS files to split.")
_parser.add_argument("--plot", action="store_true", help="Plot the split data.")
_parser.add_argument(
    "--log", type=str.upper, default="INFO", choices=get_args(LOG_LEVEL), help="Set  log level."
)
_parser.add_argument(
    "--smoothing-window",
    type=float,
    help="Smoothing window size for the filtered derivatives.",
)
_parser.add_argument(
    "--smoothing-repeat",
    type=int,
    help="Number of times to repeat the smoothing.",
)
_parser.add_argument("--overwrite", action="store_true", help="Overwrite existing output files.")


@dc.dataclass(slots=True)
class ParsedArguments:
    files: list[str]
    plot: bool
    log: LOG_LEVEL
    overwrite: bool
    smoothing_window: float
    smoothing_repeat: int


def parser_cmdline_args(args: list[str] | None = None) -> ParsedArguments:
    return _parser.parse_args(
        args,
        namespace=ParsedArguments(
            [], plot=False, log="INFO", overwrite=False, smoothing_window=50, smoothing_repeat=2
        ),
    )
