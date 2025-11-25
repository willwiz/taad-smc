from pathlib import Path
from typing import TYPE_CHECKING

from pytools.logging.api import BLogger

from ._activation import summarize_activation_data
from ._argparse import parse_arguments
from ._cycling import summarize_cycling_data
from ._initialization import import_datafiles
from ._print import log_search_results
from ._relaxation import summarize_relaxation_data

if TYPE_CHECKING:
    from pytools.logging.trait import ILogger


def main(folder: Path, *, log: ILogger) -> None:
    database = import_datafiles(folder).unwrap()
    log_search_results(database, log=log)
    summarize_activation_data(database, log=log)
    summarize_cycling_data(database, log=log)
    summarize_relaxation_data(database, log=log)


if __name__ == "__main__":
    args = parse_arguments()
    log = BLogger(args.log)
    for folder in args.folders:
        main(Path(folder) or Path(), log=log)
