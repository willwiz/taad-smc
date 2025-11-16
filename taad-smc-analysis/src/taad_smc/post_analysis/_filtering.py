from typing import TYPE_CHECKING

import numpy as np
from scipy.ndimage import gaussian_filter1d

if TYPE_CHECKING:
    from pytools.arrays import A1


def filter_segment[F: np.number](arr: A1[F], window: int) -> A1[F]:
    n_points = len(arr)
    padded_arr = np.pad(arr, (3 * window, 3 * window), mode="reflect", reflect_type="odd")
    filtered_arr = gaussian_filter1d(padded_arr, sigma=window)
    return filtered_arr[3 * window : 3 * window + n_points]
