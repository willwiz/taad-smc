import dataclasses as dc

import numpy as np
from arraystubs import Arr1


@dc.dataclass(slots=True)
class DataCurve[F: np.floating]:
    n: int
    time: Arr1[F]
    strain: Arr1[F]
