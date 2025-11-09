from pathlib import Path
from typing import TYPE_CHECKING

from pytools.logging.api import BLogger
from taad_smc.pwlsplit._tools import create_names, parser_optional_args

from ._argparse import parser_cmdline_args

if TYPE_CHECKING:
    from pytools.logging.trait import ILogger
    from taad_smc.pwlsplit._trait import SegmentOptions


def main(file: Path, opts: SegmentOptions, *, log: ILogger) -> None:
    log.info(f"Processing file: {file}")
    names = create_names(file)
    if names.csv.exists() and not opts.overwrite:
        log.info(f"Output for {file} already exists, skipping...")
        return


if __name__ == "__main__":
    args = parser_cmdline_args()
    opts = parser_optional_args(args)
    logger = BLogger(args.log)
    files = [Path(f) for name in args.files for f in Path().glob(name)]
    for file in files:
        main(file, opts=opts, log=logger)
