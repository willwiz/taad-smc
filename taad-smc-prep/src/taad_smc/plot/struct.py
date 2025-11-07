import dataclasses as dc
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from pytools.arrays import A1


@dc.dataclass
class PlotData[T: np.number]:
    x: A1[T]
    y: A1[T]
