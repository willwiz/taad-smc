from pprint import pformat
from typing import TYPE_CHECKING, Unpack

from pytools.logging.api import BLogger
from pytools.path import expanded_path_generator
from pytools.result import Err, Ok
from taad_smc.io.api import find_data_subdirectories

from ._argparse import parse_arguments, parse_options
from ._loops import protocol_generation_loop, specimen_infokey_loop
from ._types import ProgramOptions, SpecimenTree

if TYPE_CHECKING:
    from pathlib import Path

    from pytools.logging.trait import ILogger


def main(home: Path, *, log: ILogger, **opts: Unpack[ProgramOptions]) -> None:
    log.brief(f"Processing folder {home}")
    match find_data_subdirectories(home):
        case Ok(folders):
            filetree = SpecimenTree(home=home, data=folders)
            log.info(pformat(folders))
        case Err(e):
            log.error(f"Failed to find data subdirectories in {home}: {e}")
            return
    specimen_infokey_loop(filetree, log=log, **opts).unwrap()
    protocol_generation_loop(filetree, log=log, **opts).unwrap()
    log.info(f"Finished processing folder {home}")


if __name__ == "__main__":
    args = parse_arguments()
    opts = parse_options(args)
    log = BLogger(args.log)
    for f in expanded_path_generator(args.folders):
        main(f, log=log, **opts)
