import argparse
import dataclasses as dc
from typing import TYPE_CHECKING, get_args

from pytools.logging.trait import LOG_LEVEL

from ._types import FILTER_METHODS, FilterKwargs

if TYPE_CHECKING:
    from collections.abc import Sequence

_parser = argparse.ArgumentParser(
    description="Read a TDMS file and print its contents.",
)
_parser.add_argument("files", type=str, nargs="+")
_parser.add_argument("--plot", action="store_true")
_parser.add_argument("--log", type=str.upper, choices=get_args(LOG_LEVEL))
_parser.add_argument("--window", type=float, help="Window size for filtering.")
_parser.add_argument("--method", type=str.lower, choices=get_args(FILTER_METHODS))
_parser.add_argument("--export", type=str, help="Path to export filtered data.")


@dc.dataclass(slots=True)
class ParsedArguments:
    """TypedDict for command line arguments."""

    files: Sequence[str]
    window: float
    method: FILTER_METHODS
    plot: bool
    log: LOG_LEVEL
    export: str | None


def parse_args(args: list[str] | None = None) -> ParsedArguments:
    return _parser.parse_args(
        args,
        namespace=ParsedArguments(
            files=[], method="gaussian", window=101, plot=False, log="INFO", export=None
        ),
    )


def options_from_args(args: ParsedArguments) -> FilterKwargs:
    return FilterKwargs(
        method=args.method,
        window=args.window,
    )
