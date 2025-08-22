__all__ = [
    "create_curves",
    "filtered_derivatives",
    "find_first_index",
    "find_last_index",
    "generate_tags",
    "get_index_list",
    "import_test_protocol",
    "parse_cli_args",
    "plot_filtered",
    "segment_duration",
]
from collections.abc import Mapping, Sequence
from pathlib import Path
from pprint import pformat

import numpy as np
from pytools.logging.trait import NULL_LOG, ILogger

from ._index import find_first_index, find_last_index, get_index_list
from ._io import import_test_protocol
from ._parser import parser
from ._plotting import plot_filtered
from ._protocol import aligned_curve_indices, create_curve, generate_tags
from ._segment import filtered_derivatives, segment_duration
from .struct import TAADCurve
from .trait import Arguments, TestProtocol


def parse_cli_args(args: list[str] | None = None) -> Arguments:
    """Parse command line arguments."""
    files = [v for val in parser.parse_args(args).file for v in Path().glob(val)]
    return {"file": files}


def create_curves(
    protocol: Mapping[str, TestProtocol],
    start_idx: int = 0,
    *,
    log: ILogger = NULL_LOG,
) -> Mapping[str, Sequence[TAADCurve[np.float64, np.intp]]]:
    """Create curves from the protocol."""
    curves = {k: create_curve(v) for k, v in protocol.items()}
    aligned_curves = aligned_curve_indices(curves, start_idx=start_idx)
    log.debug("Curves:", pformat(aligned_curves, indent=2, sort_dicts=False))
    return aligned_curves
