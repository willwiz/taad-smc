__all__ = ["create_curves"]
from collections.abc import Mapping, Sequence
from pathlib import Path

import numpy as np
from arraystubs import Arr1

from .struct import Segmentation, TAADCurve
from .trait import Arguments, TestProtocol

def parse_cli_args(args: list[str] | None = None) -> Arguments: ...
def create_curves(
    protocol: Mapping[str, TestProtocol],
    start_idx: int = 0,
) -> Mapping[str, Sequence[TAADCurve[np.float64, np.intp]]]: ...
def generate_tags(
    curves: Mapping[str, Sequence[TAADCurve[np.float64, np.intp]]],
) -> Sequence[tuple[str, int, str]]: ...
def import_test_protocol(file: Path) -> Mapping[str, TestProtocol]: ...
def find_first_index[F: np.floating](arr: Arr1[F], *, tol: float = 1.0e-6) -> int: ...
def find_last_index[F: np.floating](arr: Arr1[F], *, tol: float = 1.0e-6) -> int: ...
def get_index_list[F: np.floating, I: np.integer](
    curves: Mapping[str, Sequence[TAADCurve[F, I]]],
    length: int,
) -> Segmentation[I]: ...
