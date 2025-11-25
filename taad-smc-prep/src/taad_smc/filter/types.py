import dataclasses as dc
from typing import TYPE_CHECKING, Literal, Required, TypedDict

import numpy as np

if TYPE_CHECKING:
    from pytools.arrays import A1

__all__ = ["FILTER_METHODS"]
FILTER_METHODS = Literal["gaussian", "median", "mean"]


class FilterKwargs(TypedDict, total=False):
    window: Required[float]
    method: Required[FILTER_METHODS]


class FilterOptions(TypedDict, total=False):
    method: FILTER_METHODS
    window: float


@dc.dataclass(frozen=True)
class PlotData[F: np.number]:
    x: A1[F]
    y: A1[F]
