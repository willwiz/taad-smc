import argparse
from typing import get_args

from pytools.logging.trait import LOG_LEVEL

from ._types import ParsedArguments, ProgramOptions

__all__ = ["parse_arguments"]


_parser = argparse.ArgumentParser("summary", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
_parser.add_argument("folders", type=str, nargs="+", help="Input data folders")
_parser.add_argument("--log", type=str.upper, choices=get_args(LOG_LEVEL))
_parser.add_argument("--overwrite", action="store_true")


def parse_arguments(args: list[str] | None = None) -> ParsedArguments:
    return _parser.parse_args(args=args, namespace=ParsedArguments([], overwrite=False, log="INFO"))


def parse_options(args: ParsedArguments) -> ProgramOptions:
    return {"overwrite": args.overwrite}
