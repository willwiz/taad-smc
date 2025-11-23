import dataclasses as dc
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from pytools.arrays import A1


@dc.dataclass(slots=True)
class DataCurve[F: np.floating]:
    n: int
    time: A1[F]
    strain: A1[F]
