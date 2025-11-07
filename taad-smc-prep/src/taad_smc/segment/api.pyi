from collections.abc import Mapping, Sequence
from pathlib import Path

import numpy as np
from pytools.arrays import A1
from pytools.logging.trait import ILogger

from .struct import DataSeries, Segmentation, TAADCurve
from .trait import TestProtocol

def create_curves(
    protocol: Mapping[str, TestProtocol],
    start_idx: int = 0,
    *,
    log: ILogger = ...,
) -> Mapping[str, Sequence[TAADCurve[np.float64, np.intp]]]: ...
def generate_tags(
    curves: Mapping[str, Sequence[TAADCurve[np.float64, np.intp]]],
) -> Sequence[tuple[str, int, str]]: ...
def import_test_protocol(file: Path | str) -> Mapping[str, TestProtocol]: ...
def find_first_index[F: np.floating](
    arr: A1[F],
    *,
    tol: float = 1.0e-6,
    log: ILogger = ...,
) -> int: ...
def find_last_index[F: np.floating](
    arr: A1[F],
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
    time: A1[F],
    disp: A1[F],
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
def plot_filtered[F: np.floating](
    data: DataSeries[F],
    fout: Path,
) -> None: ...
