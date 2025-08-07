import dataclasses as dc
from collections.abc import Sequence
from typing import Literal

import numpy as np
from arraystubs import Arr1


@dc.dataclass(slots=True)
class TAADCurve[F: np.floating, I: np.integer]:
    """Data structure for TAAD curve."""

    nth: int
    idx: Arr1[I]
    order: Arr1[I]
    time: Arr1[F]
    disp: Arr1[F]
    curve: Sequence[Literal["Stretch", "Hold", "Recover"]]


@dc.dataclass(slots=True)
class TAADProtocol[F: np.floating, I: np.integer]:
    """Data structure for TAAD protocol."""

    strain: float
    sample_rate: int
    curves: Sequence[TAADCurve[F, I]]


@dc.dataclass(slots=True)
class Split:
    idx: int
    kind: Literal["PEAK", "VALLEY"]


@dc.dataclass(slots=True)
class Segmentation[I: np.integer]:
    idx: Arr1[I]
    # kind: Sequence[Literal["PEAK", "VALLEY"]]
