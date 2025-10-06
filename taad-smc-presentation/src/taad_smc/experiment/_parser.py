# Copyright (c) 2025 Will Zhang

import dataclasses as dc
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser

from pytools.logging.trait import LogLevel

__all__ = ["parse_arguments"]

parser = ArgumentParser("Pre-analysis for TAAD-SMC", formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("files", type=str, nargs="+", help="Input data files (CSV format)")
parser.add_argument(
    "--log",
    type=str.upper,
    default="NULL",
    choices=("NULL", "ERROR", "WARNING", "BRIEF", "INFO", "DEBUG"),
    help="Log level",
)


@dc.dataclass(slots=True, frozen=True)
class PreAnalysisArguments:
    files: list[str]
    log: LogLevel


def parse_arguments() -> PreAnalysisArguments:
    args = parser.parse_args()
    return PreAnalysisArguments(files=args.files, log=LogLevel[args.log])
