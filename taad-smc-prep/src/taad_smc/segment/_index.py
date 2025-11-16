import itertools
from pprint import pformat
from typing import TYPE_CHECKING

import numpy as np
from pytools.logging.api import NLOGGER
from scipy.ndimage import gaussian_filter1d

from .struct import Segmentation, TAADCurve
from .trait import CurvePoint, CurveSegment

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from pytools.arrays import A1
    from pytools.logging.trait import ILogger


def _is_peak(
    left: CurveSegment,
    right: CurveSegment,
) -> CurvePoint:
    match (left, right):
        case _, CurveSegment.STRETCH:
            return CurvePoint.PEAK
        case _, CurveSegment.RECOVER:
            return CurvePoint.VALLEY
        case CurveSegment.STRETCH, CurveSegment.HOLD:
            return CurvePoint.VALLEY
        case CurveSegment.RECOVER, CurveSegment.HOLD:
            return CurvePoint.PEAK
        case CurveSegment.HOLD, CurveSegment.HOLD:
            msg = "Consecutive 'Hold' segments found."
            raise ValueError(msg)


def get_index_list[F: np.floating, I: np.integer](
    curves: Mapping[str, Sequence[TAADCurve[F, I]]],
    length: int,
    *,
    log: ILogger = NLOGGER,
) -> Segmentation[I, np.float64]:
    index_as_intp = np.unique(
        np.array(
            [0] + [v for curve in curves.values() for c in curve for v in c.idx] + [length],
            dtype=curves[next(iter(curves))][0].idx.dtype,
        ),
    )
    curve_kinds = [
        CurveSegment.HOLD,
        *[v for curve in curves.values() for c in curve for v in c.curve],
        CurveSegment.HOLD,
    ]
    rates = np.array(
        [
            0,
            *[v for curve in curves.values() for c in curve for v in c.slope],
            0,
        ],
    )
    rates = np.array(
        [
            0,
            *[5000 * (b - a) for a, b in itertools.pairwise(rates)],
            0,
        ],
        dtype=np.float64,
    )
    rates = rates / rates.max()
    kinds = (
        [CurvePoint.VALLEY]
        + [_is_peak(left, right) for left, right in itertools.pairwise(curve_kinds)]
        + [CurvePoint.VALLEY]
    )
    log.info("Last index:", index_as_intp[-1])
    log.debug(
        f"Main index (n = {len(index_as_intp)}):",
        pformat(index_as_intp, indent=2, sort_dicts=False),
        f"kinds (n = {len(kinds)}):",
        pformat(kinds, indent=2, sort_dicts=False),
    )
    return Segmentation(
        idx=index_as_intp,
        kind=kinds,
        rate=rates,
    )


def find_first_index[F: np.floating](
    arr: A1[F],
    *,
    tol: float = 1.0e-6,
    log: ILogger = NLOGGER,
) -> int:
    """Find the first index of a non-zero element in a 1D array."""
    filtered = arr - arr[0:100].mean()
    i = 0
    for i in range(len(filtered)):
        if filtered[i] > tol:
            break
    log.info(f"First index: {i}")
    return i


def find_last_index[F: np.floating](
    arr: A1[F],
    *,
    tol: float = 1.0e-6,
    log: ILogger = NLOGGER,
) -> int:
    """Find the last index of a non-zero element in a 1D array."""
    filtered = gaussian_filter1d(arr, sigma=100)
    i = len(filtered) - 1
    for i in range(len(filtered) - 1, -1, -1):
        if filtered[i] > tol:
            break
    log.info(f"Last index: {i}")
    return i
