from typing import TYPE_CHECKING

from pytools.logging.api import BLogger
from pytools.path import expand_as_path
from taad_smc.io.api import import_df

from ._argparse import options_from_args, parse_args
from ._filtering import filter_curves
from ._tools import find_split_points, plot_loop

if TYPE_CHECKING:
    from pathlib import Path

    from pytools.logging.trait import ILogger

    from ._types import FilterKwargs


def main(file: Path, *, fout: str | None, opt: FilterKwargs, log: ILogger) -> None:
    log.info(f"Trying out filter for file: {file}")
    if fout and (file.parent / fout).exists():
        log.info(f"Output file {fout} already exists skipping...")
        return
    df = import_df(file).unwrap()
    split_points = find_split_points(df, ["protocol", "cycle", "mode"])
    ff = filter_curves(df, cols=["force", "disp"], index=split_points, **opt).unwrap()
    figname = file.with_name(f"Filtered_{opt['method'].capitalize()}.png")
    plot_loop(df, ff, fout=figname).unwrap()
    if fout:
        log.info(f"Exported filtered data to: {fout}")
        ff.to_csv(file.parent / fout, sep="\t", index=False)


if __name__ == "__main__":
    args = parse_args()
    opts = options_from_args(args)
    files = expand_as_path(args.files)
    log = BLogger(args.log)
    if not files:
        log.warn("No input files provided. Exiting.")
    for file in files:
        main(file, fout=args.export, opt=opts, log=log)
