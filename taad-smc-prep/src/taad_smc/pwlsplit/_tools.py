from typing import TYPE_CHECKING

from pytools.logging.trait import LogLevel
from taad_smc.pwlsplit._trait import FileNames, SegmentOptions

if TYPE_CHECKING:
    from pathlib import Path

    from ._argparse import ParsedArguments


def parser_optional_args(args: ParsedArguments) -> SegmentOptions:
    return SegmentOptions(plot=args.plot, overwrite=args.overwrite, log=LogLevel[args.log])


def create_names(file: Path) -> FileNames:
    parent = file.parent
    return FileNames(
        raw=file,
        csv=file.with_suffix(".csv"),
        protocol=(parent / "protocol.json"),
        info=(parent / "key.json"),
    )
