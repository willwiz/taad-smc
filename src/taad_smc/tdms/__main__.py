import argparse
from collections.abc import Sequence
from pathlib import Path
from typing import TypedDict

from .api import export_tdms, import_tdms_raw

parser = argparse.ArgumentParser(
    description="Read a TDMS file and print its contents.",
)
parser.add_argument("file", type=str, nargs="+", help="Path to the TDMS file to read.")


class Arguments(TypedDict):
    """TypedDict for command line arguments."""

    file: Sequence[Path]


def parse_args(args: list[str] | None = None) -> Arguments:
    """Parse command line arguments."""
    return {"file": [v for val in parser.parse_args(args).file for v in Path().glob(val)]}


def main(file: str | Path) -> None:
    file = Path(file)
    data = import_tdms_raw(file)
    export_tdms(data, file)


if __name__ == "__main__":
    args = parse_args()
    for f in args["file"]:
        main(f)
