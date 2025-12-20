from typing import TYPE_CHECKING

from pytools.logging.api import BLogger
from pytools.path import expand_as_path
from taad_smc.io.api import import_specimen_info

from ._activation import summarize_activation_data
from ._argparse import parse_arguments
from ._cycling import summarize_activated_cycling_data, summarize_cycling_data
from ._initialization import import_datafiles
from ._plotting import create_legend_on_axis, create_ppgrid, save_and_close_fig
from ._print import log_search_results
from ._relaxation import summarize_relaxation_data
from ._stats import summarize_peak_data
from ._tools import search_for_ylim

if TYPE_CHECKING:
    from pathlib import Path

    from pytools.logging.trait import ILogger


def main(folder: Path, *, log: ILogger) -> None:
    log.brief(f"Generating summary for folder: {folder}")
    database = import_datafiles(folder).unwrap()
    spec_info = import_specimen_info(folder / "key.json").unwrap()
    ylim = search_for_ylim(database).unwrap()
    log_search_results(database, log=log)
    super_title = (
        f"TAAD-SMC {spec_info['species']} {folder.parent.name}"
        f" - {folder.name.capitalize()}. Summary"
    )
    fig, axes = create_ppgrid(title=super_title)
    create_legend_on_axis(axes[0][0])
    summarize_activation_data(axes, database, log=log, ylim=ylim)
    summarize_peak_data(axes, database, log=log)
    summarize_cycling_data(axes, database, log=log, ylim=ylim)
    summarize_activated_cycling_data(axes, database, log=log, ylim=ylim)
    summarize_relaxation_data(axes, database, log=log, ylim=ylim)
    save_and_close_fig(fig, folder / "summary.png", dpi=300)
    log.brief(f"Saved summary figure to: {folder / 'summary.png'}")


if __name__ == "__main__":
    args = parse_arguments()
    log = BLogger(args.log)
    for folder in expand_as_path(args.folders):
        main(folder, log=log)
