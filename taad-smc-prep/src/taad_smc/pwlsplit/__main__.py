from pathlib import Path
from pprint import pformat
from typing import TYPE_CHECKING

from pytools.logging.api import BLogger
from pytools.result import Err, Ok

from ._argparse import parser_cmdline_args
from ._io import import_data
from ._tools import create_names, parser_optional_args

if TYPE_CHECKING:
    from pytools.logging.trait import ILogger

    from ._trait import SegmentOptions


def main(file: Path, opts: SegmentOptions, *, log: ILogger) -> None:
    log.info(f"Processing file: {file}")
    log.debug(f"Options: {opts}")
    match create_names(file):
        case Ok(names):
            pass
        case Err(e):
            raise e
    if names.csv.exists() and not opts.overwrite:
        log.info(f"Output for {file} already exists, skipping...")
        return
    match import_data(names, log=log):
        case Err(e):
            raise e
        case Ok((data, protocol, info)):
            log.debug(pformat(data, sort_dicts=False))
            log.debug(pformat(info, sort_dicts=False))
            log.debug(pformat(protocol, sort_dicts=False))


if __name__ == "__main__":
    args = parser_cmdline_args()
    opts = parser_optional_args(args)
    logger = BLogger(args.log)
    files = [Path(f) for name in args.files for f in Path().glob(name)]
    for file in files:
        main(file, opts=opts, log=logger)
