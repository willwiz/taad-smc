from typing import TYPE_CHECKING

from pytools.logging.trait import LogLevel
from pytools.result import Err, Ok
from taad_smc.pwlsplit._trait import FileNames, SegmentOptions

if TYPE_CHECKING:
    from pathlib import Path

    from ._argparse import ParsedArguments


def parser_optional_args(args: ParsedArguments) -> SegmentOptions:
    return SegmentOptions(plot=args.plot, overwrite=args.overwrite, log=LogLevel[args.log])


def create_names(file: Path) -> Ok[FileNames] | Err:
    parent = file.parent
    match (parent / "protocol.json").exists():
        case False:
            return Err(FileExistsError(f"File {parent / 'protocol.json'} does not exist."))
        case True:
            protocol = parent / "protocol.json"
    match (parent / "key.json").exists():
        case False:
            return Err(FileExistsError(f"File {parent / 'key.json'} does not exist."))
        case True:
            info = parent / "key.json"
    return Ok(
        FileNames(
            raw=file,
            csv=file.with_suffix(".csv"),
            protocol=protocol,
            info=info,
        )
    )
