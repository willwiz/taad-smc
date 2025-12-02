from itertools import pairwise
from math import ceil
from typing import TYPE_CHECKING, Protocol, Unpack

import numpy as np
from pytools.result import Err, Ok
from scipy.ndimage import gaussian_filter1d, median_filter

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping

    import pandas as pd
    from pytools.arrays import A1

    from ._types import FILTER_METHODS, FilterKwargs


class _FilterCallable(Protocol):
    def __call__[F: np.number](self, arr: A1[F], window: float) -> A1[F]: ...


def _gaussian_filter[F: np.number](arr: A1[F], window: float) -> A1[F]:
    return gaussian_filter1d(arr, sigma=window)


def _median_filter[F: np.number](arr: A1[F], window: float) -> A1[F]:
    return median_filter(arr, size=int(window))


FILTERS: Mapping[FILTER_METHODS, _FilterCallable] = {
    "gaussian": _gaussian_filter,
    "median": _median_filter,
}


def filter_curve_segment[F: np.number](
    arr: A1[F], **kwargs: Unpack[FilterKwargs]
) -> Ok[A1[F]] | Err:
    n_points = len(arr)
    window = ceil(kwargs.get("window"))
    if not window:
        return Err(NameError("`window` parameter is a required keyword argument"))
    padded_arr = np.pad(arr, (3 * window, 3 * window), mode="reflect", reflect_type="odd")
    method = kwargs.get("method", "gaussian")
    match FILTERS.get(method):
        case None:
            return Err(ValueError(f"No filter implementation found for method={method}"))
        case filter:
            filtered_arr = filter(padded_arr, window=window)
    return Ok(filtered_arr[3 * window : 3 * window + n_points])


def filter_curves_i(
    df: pd.DataFrame, col: str, index: Iterable[int], **kwargs: Unpack[FilterKwargs]
) -> Ok[pd.DataFrame] | Err:
    array = df[[col]].to_numpy(np.float64).flatten()
    for i, j in pairwise(index):
        match filter_curve_segment(array[i:j], **kwargs):
            case Ok(filtered_segment):
                array[i:j] = filtered_segment
            case Err(e):
                return Err(e)
    df[col] = array
    return Ok(df)


def filter_curves(
    df: pd.DataFrame,
    cols: Iterable[str],
    *,
    index: Iterable[int] | None = None,
    **kwargs: Unpack[FilterKwargs],
) -> Ok[pd.DataFrame] | Err:
    index = (0, len(df)) if index is None else index
    filtered_df = df.copy()
    for c in cols:
        match filter_curves_i(filtered_df, c, index, **kwargs):
            case Ok(filtered_df):
                pass
            case Err(e):
                return Err(e)
    return Ok(filtered_df)
