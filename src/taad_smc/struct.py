import dataclasses as dc
import traceback

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


class Error:
    msg: str
    trace: traceback.StackSummary

    def __init__(self, msg: str) -> None:
        self.msg = msg
        self.trace = traceback.extract_stack()
