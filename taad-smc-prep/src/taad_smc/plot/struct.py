import dataclasses as dc
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from arraystubs import Arr1


@dc.dataclass
class PlotData[T: np.number]:
    x: Arr1[T]
    y: Arr1[T]
