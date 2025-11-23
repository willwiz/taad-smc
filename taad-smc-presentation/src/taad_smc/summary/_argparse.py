import argparse
import dataclasses as dc
from typing import get_args

from pytools.logging.trait import LOG_LEVEL

__all__ = ["parse_arguments"]


_parser = argparse.ArgumentParser("summary", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
_parser.add_argument("folders", type=str, nargs="+", help="Input data folders")
_parser.add_argument(
    "--log",
    type=str.upper,
    choices=get_args(LOG_LEVEL),
    help="Log level",
)


@dc.dataclass(slots=True)
class ParsedArguments:
    folders: list[str]
    log: LOG_LEVEL


def parse_arguments(args: list[str] | None = None) -> ParsedArguments:
    return _parser.parse_args(args=args, namespace=ParsedArguments([], "INFO"))
