from pathlib import Path
from typing import TYPE_CHECKING

from pytools.logging.api import BLogger

from ._argparse import parse_arguments
from ._initialization import import_datafiles
from ._print import log_search_results

if TYPE_CHECKING:
    from pytools.logging.trait import ILogger


def main(folder: Path, *, log: ILogger) -> None:
    database = import_datafiles(folder).unwrap()
    log_search_results(database, log=log)


if __name__ == "__main__":
    args = parse_arguments()
    log = BLogger(args.log)
    for folder in args.folders:
        main(Path(folder) or Path(), log=log)
