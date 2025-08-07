import dataclasses as dc

import numpy as np
from arraystubs import Arr1


@dc.dataclass
class PlotData[T: np.number]:
    x: Arr1[T]
    y: Arr1[T]
