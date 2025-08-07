import argparse

from .struct import ParsedArgs

parser = argparse.ArgumentParser(
    description="convert TDMS files to CSV format",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "input_file",
    type=str,
    nargs="+",
    help="input TDMS file(s) to convert",
)
parser.add_argument(
    "--output_file",
    "-o",
    type=str,
    default=None,
    help="output CSV file name (default: same as input file with .csv extension)",
)


def get_argument_from_cmdline(args: list[str] | None = None) -> ParsedArgs:
    """Parse command line arguments and return a ParserArgs object.

    Parameters
    ----------
    args : list[str] | None, optional
        List of command line arguments. If None, uses sys.argv[1:].

    Returns
    -------
    ParsedArgs
        An object containing parsed command line arguments.

    """
    parsed_values = parser.parse_args(args)
    return ParsedArgs(
        input_file=parsed_values.input_file,
        output_file=parsed_values.output_file,
    )
