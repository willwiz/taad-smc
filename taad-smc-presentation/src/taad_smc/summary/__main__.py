from pathlib import Path
from typing import TYPE_CHECKING

from pytools.logging.api import BLogger
from taad_smc.summary._plotting import create_ppgrid, save_and_close_fig

from ._activation import summarize_activation_data
from ._argparse import parse_arguments
from ._cycling import summarize_activated_cycling_data
from ._initialization import import_datafiles
from ._print import log_search_results
from ._relaxation import summarize_relaxation_data

if TYPE_CHECKING:
    from pytools.logging.trait import ILogger


def main(folder: Path, *, log: ILogger) -> None:
    database = import_datafiles(folder).unwrap()
    log_search_results(database, log=log)
    fig, axes = create_ppgrid()
    summarize_activation_data(axes, database, log=log)
    summarize_activated_cycling_data(axes, database, log=log)
    summarize_relaxation_data(axes, database, log=log)
    save_and_close_fig(fig, folder / "summary.png", dpi=300)


if __name__ == "__main__":
    args = parse_arguments()
    log = BLogger(args.log)
    for folder in args.folders:
        main(Path(folder) or Path(), log=log)
