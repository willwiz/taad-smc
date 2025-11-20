from pathlib import Path
from pprint import pformat
from typing import TYPE_CHECKING

from pytools.logging.api import BLogger

from pwlsplit.curve.peaks import construct_initial_segmentation
from pwlsplit.plot import plot_prepped_data
from pwlsplit.segment.refine import opt_index

from ._argparse import parser_cmdline_args
from ._io import import_data
from ._loops import segmentation_loop
from ._tools import (
    compile_taadsmc_curves,
    construct_postprocessed_df,
    create_names,
    filter_derivative,
    parser_optional_args,
)

if TYPE_CHECKING:
    from pytools.logging.trait import ILogger

    from ._trait import SegmentOptions


def main(file: Path, opts: SegmentOptions, *, log: ILogger) -> None:
    log.brief(f"Processing file: {file}")
    log.info("Options:", pformat(opts, sort_dicts=False))
    names = create_names(file).unwrap()
    if names.csv.exists() and not opts.overwrite:
        log.info(f"Output for {file} already exists, skipping...")
        return
    log.info("Importing data...")
    data, protocol, info = import_data(names, log=log).unwrap()
    log.info("Data imported successfully.")
    log.debug(pformat(data, sort_dicts=False))
    log.debug(pformat(info, sort_dicts=False))
    log.debug(pformat(protocol, sort_dicts=False))
    log.info("Filtering derivative...")
    prepped_data = filter_derivative(data.disp, window=opts.window, repeat=opts.repeat)
    log.info("Plotting prepped data...")
    plot_prepped_data(prepped_data, fout=names.parent / "FindPeaks_prepped.png")
    protocol_map, curves = compile_taadsmc_curves(protocol).unwrap()
    log.info("Protocol constructed successfully.")
    log.debug(pformat(protocol_map, sort_dicts=False))
    log.debug(pformat(curves, sort_dicts=False))
    log.info("Constructing initial segmentation...")
    segmentation = construct_initial_segmentation(curves).unwrap()
    log.debug(pformat(segmentation, sort_dicts=False))
    fparent = names.parent if opts.plot else None
    segmentation = segmentation_loop(
        protocol_map, segmentation, prepped_data, log=log, fparent=fparent
    ).unwrap()
    log.info("Refining segmentation...")
    segmentation.idx = opt_index(
        prepped_data.x, segmentation.idx, window=int(opts.window), max_iter=100, log=log
    )
    df = construct_postprocessed_df(data, info, protocol_map, segmentation)
    df.to_csv(names.csv, index=False)
    log.brief(f"Final segmentation (n={len(data.time)}) complete.")


if __name__ == "__main__":
    args = parser_cmdline_args()
    opts = parser_optional_args(args)
    logger = BLogger(args.log)
    files = [Path(f) for name in args.files for f in Path().glob(name)]
    if not files:
        logger.error("No input files found. with input patterns: ", args.files)
    for file in files:
        main(file, opts=opts, log=logger)
