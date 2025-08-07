import dataclasses as dc

import numpy as np
from arraystubs import Arr1


@dc.dataclass(slots=True)
class AortaData:
    protocol: Arr1[np.str_]
    cycle: Arr1[np.intp]
    mode: Arr1[np.str_]
    time: Arr1[np.float64]
    disp: Arr1[np.float64]
    force: Arr1[np.float64]
