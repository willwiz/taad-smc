__all__ = [
    "create_curves",
    "find_first_index",
    "find_last_index",
    "generate_tags",
    "get_index_list",
    "import_test_protocol",
    "parse_cli_args",
]
from collections.abc import Mapping, Sequence
from pathlib import Path

import numpy as np

from ._index import find_first_index, find_last_index, get_index_list
from ._io import import_test_protocol
from ._parser import parser
from ._protocol import aligned_curve_indices, create_curve, generate_tags
from .struct import TAADCurve
from .trait import Arguments, TestProtocol


def parse_cli_args(args: list[str] | None = None) -> Arguments:
    """Parse command line arguments."""
    files = [v for val in parser.parse_args(args).file for v in Path().glob(val)]
    return {"file": files}


def create_curves(
    protocol: Mapping[str, TestProtocol],
    start_idx: int = 0,
) -> Mapping[str, Sequence[TAADCurve[np.float64, np.intp]]]:
    """Create curves from the protocol."""
    curves = {k: create_curve(v) for k, v in protocol.items()}
    return aligned_curve_indices(curves, start_idx=start_idx)
