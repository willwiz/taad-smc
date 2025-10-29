# Copyright (c) 2025 Will Zhang

from pathlib import Path
from pprint import pformat
from typing import TYPE_CHECKING

from pytools.logging.api import NLOGGER, BLogger
from taad_smc.segment._refinement import opt_index

from ._index import find_first_index, get_index_list
from ._io import construct_postprocessed_df, import_data
from ._parser import parser
from ._plotting import plot_filtered
from ._protocol import create_curves, generate_tags
from ._segment import filtered_derivatives, segment_duration

if TYPE_CHECKING:
    from pytools.logging.trait import ILogger

    from .trait import Arguments


def parse_cli_args(args: list[str] | None = None) -> Arguments:
    """Parse command line arguments."""
    files = [v for val in parser.parse_args(args).file for v in Path().glob(val)]
    return {"file": files}


def main(file: Path, *, log: ILogger = NLOGGER) -> None:
    log.info(f"Processing file: {file}")
    if file.with_suffix(".csv").exists():
        log.info(f"Output for {file} already exists, skipping...")
        return
    data, protocol = import_data(file, log=log)
    if not protocol:
        log.info(f"No protocol found in {file}, skipping...")
        return
    data.disp = data.disp - data.disp[0]
    filtered_data = filtered_derivatives(data.time, data.disp, smoothing_window=50, repeat=5)
    plot_filtered(filtered_data, fout=file.parent / "filtered_plot.png")
    first_idx = find_first_index(filtered_data.x, tol=1e-2, log=log)
    curves = create_curves(protocol, start_idx=first_idx, log=log)
    log.debug("Curves created successfully.", pformat(curves, indent=2, sort_dicts=False))
    curves_tags = generate_tags(curves)
    main_index = get_index_list(curves, length=filtered_data.x.size, log=log)
    log.debug("Main index created successfully.", pformat(main_index, indent=2, sort_dicts=False))
    for k, v in curves.items():
        log.info(f"Processing {k} with {len(v)} curves.")
        main_index = segment_duration(
            filtered_data,
            v,
            main_index,
            fout=file.parent / f"Findpeak_{k}_transition.png",
            log=log,
        )
    log.debug(f"final protocol {len(data.time)}:", format(main_index.idx))
    log.info("Optimizing main index...")
    new_index = opt_index(data.disp, main_index.idx, windows=50, log=log)
    main_index.idx = new_index
    df = construct_postprocessed_df(data, main_index, curves_tags)
    df.to_csv(file.with_suffix(".csv"), index=False)


if __name__ == "__main__":
    args = parse_cli_args()
    log = BLogger("INFO")
    for file in args["file"]:
        main(file, log=log)
