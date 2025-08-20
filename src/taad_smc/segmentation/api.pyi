__all__ = ["create_curves"]
from collections.abc import Mapping, Sequence
from pathlib import Path

import numpy as np
from arraystubs import Arr1
from pytools.logging.trait import ILogger

from .struct import DataSeries, Segmentation, TAADCurve
from .trait import Arguments, TestProtocol

def parse_cli_args(args: list[str] | None = None) -> Arguments: ...
def create_curves(
    protocol: Mapping[str, TestProtocol],
    start_idx: int = 0,
    *,
    log: ILogger = ...,
) -> Mapping[str, Sequence[TAADCurve[np.float64, np.intp]]]: ...
def generate_tags(
    curves: Mapping[str, Sequence[TAADCurve[np.float64, np.intp]]],
) -> Sequence[tuple[str, int, str]]: ...
def import_test_protocol(file: Path) -> Mapping[str, TestProtocol]: ...
def find_first_index[F: np.floating](
    arr: Arr1[F],
    *,
    tol: float = 1.0e-6,
    log: ILogger = ...,
) -> int: ...
def find_last_index[F: np.floating](
    arr: Arr1[F],
    *,
    tol: float = 1.0e-6,
    log: ILogger = ...,
) -> int: ...
def get_index_list[F: np.floating, I: np.integer](
    curves: Mapping[str, Sequence[TAADCurve[F, I]]],
    length: int,
    *,
    log: ILogger = ...,
) -> Segmentation[I, F]: ...
def filtered_derivatives[F: np.floating](
    time: Arr1[F],
    disp: Arr1[F],
    *,
    smoothing_window: int = 50,
    repeat: int = 5,
) -> DataSeries[F]: ...
def segment_duration[F: np.floating, I: np.integer](
    data: DataSeries[F],
    curves: Sequence[TAADCurve[F, I]],
    seg: Segmentation[I, F],
    *,
    fout: Path,
    log: ILogger = ...,
) -> Segmentation[I, F]: ...
