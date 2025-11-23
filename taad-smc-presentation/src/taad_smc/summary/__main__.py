from pathlib import Path
from typing import TYPE_CHECKING

from pytools.logging.api import BLogger

from ._argparse import parse_arguments
from ._print import print_datafound
from ._tools import find_datafiles

if TYPE_CHECKING:
    from pytools.logging.trait import ILogger


def main(folder: Path, *, log: ILogger) -> None:
    files = find_datafiles(folder).unwrap()
    print_datafound(files, log=log)


if __name__ == "__main__":
    args = parse_arguments()
    log = BLogger("INFO")
    for folder in args.folders:
        main(Path(folder) or Path(), log=log)
