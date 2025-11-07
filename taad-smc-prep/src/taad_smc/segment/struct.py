import dataclasses as dc
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from collections.abc import Sequence

    from pytools.arrays import A1
    from taad_smc.segment.trait import CurvePoint, CurveSegment


@dc.dataclass(slots=True)
class TAADCurve[F: np.floating, I: np.integer]:
    """Data structure for TAAD curve."""

    nth: int
    idx: A1[I]
    order: A1[I]
    time: A1[F]
    disp: A1[F]
    slope: A1[F]
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
    idx: A1[I]
    kind: Sequence[CurvePoint]
    rate: A1[F]


@dc.dataclass(slots=True)
class DataSeries[F: np.floating]:
    x: A1[F]
    y: A1[F]
    z: A1[F]
    dz: A1[F]
    ddz: A1[F]
