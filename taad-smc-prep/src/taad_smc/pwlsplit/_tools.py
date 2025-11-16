from typing import TYPE_CHECKING

from pytools.logging.trait import LogLevel
from pytools.result import Err, Ok

from ._trait import FileNames, SegmentOptions

if TYPE_CHECKING:
    from pathlib import Path

    from ._argparse import ParsedArguments


def parser_optional_args(args: ParsedArguments) -> SegmentOptions:
    return SegmentOptions(plot=args.plot, overwrite=args.overwrite, log=LogLevel[args.log])


def create_names(file: Path) -> Ok[FileNames] | Err:
    parent = file.parent
    if not (parent / "protocol.json").exists():
        return Err(FileExistsError(f"File {parent / 'protocol.json'} does not exist."))
    if not (parent / "key.json").exists():
        return Err(FileExistsError(f"File {parent / 'key.json'} does not exist."))
    return Ok(
        FileNames(
            raw=file,
            csv=file.with_suffix(".csv"),
            protocol=parent / "protocol.json",
            info=parent / "key.json",
        )
    )
