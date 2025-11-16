import dataclasses as dc
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from pathlib import Path

    from pytools.arrays import A1
    from pytools.logging.trait import LogLevel


@dc.dataclass(slots=True)
class SegmentOptions:
    plot: bool
    overwrite: bool
    log: LogLevel


@dc.dataclass(slots=True)
class FileNames:
    raw: Path
    csv: Path
    protocol: Path
    info: Path


@dc.dataclass(slots=True)
class DataSeries[F: np.floating]:
    x: A1[F]
    y: A1[F]
    z: A1[F]
    dz: A1[F]
    ddz: A1[F]
