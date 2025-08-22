import dataclasses as dc
from collections.abc import Sequence

import numpy as np
from arraystubs import Arr1

from taad_smc.segmentation.trait import CurvePoint, CurveSegment


@dc.dataclass(slots=True)
class TAADCurve[F: np.floating, I: np.integer]:
    """Data structure for TAAD curve."""

    nth: int
    idx: Arr1[I]
    order: Arr1[I]
    time: Arr1[F]
    disp: Arr1[F]
    slope: Arr1[F]
    curve: Sequence[CurveSegment]


@dc.dataclass(slots=True)
class TAADProtocol[F: np.floating, I: np.integer]:
    """Data structure for TAAD protocol."""

    strain: float
    sample_rate: int
    curves: Sequence[TAADCurve[F, I]]


@dc.dataclass(slots=True)
class Split:
    idx: int
    kind: CurvePoint


@dc.dataclass(slots=True)
class Segmentation[I: np.integer, F: np.floating]:
    idx: Arr1[I]
    kind: Sequence[CurvePoint]
    rate: Arr1[F]


@dc.dataclass(slots=True)
class DataSeries[F: np.floating]:
    x: Arr1[F]
    y: Arr1[F]
    z: Arr1[F]
    dz: Arr1[F]
    ddz: Arr1[F]
