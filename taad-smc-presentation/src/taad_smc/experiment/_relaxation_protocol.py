# pyright: reportUnknownMemberType = false
from typing import TypedDict, Unpack

import numpy as np

from .types import DataCurve


class RelaxationProtocolKwargs(TypedDict, total=False):
    initial_time: float
    unloading_period: float


def relaxation_protocol(
    max_strain: float,
    period: float,
    duration: float,
    dt: float,
    **kwargs: Unpack[RelaxationProtocolKwargs],
) -> DataCurve[np.float64]:
    """Generate a relaxation protocol data curve.

    Parameters
    ----------
    max_strain : float
        The maximum strain value.
    period : float
        The period of one cycle.
    duration : float
        The duration to hold the maximum strain.
    dt : float
        The time step for the generated data.
    **kwargs : CyclicLoadingProtocolKwargs
        Additional keyword arguments.
        - initial_time : float, optional
            The initial time offset (default is 0.0).
        - unloading_period : float, optional
            The unloading period after holding the maximum strain (default is equal to `period`).

    Returns
    -------
    DataCurve[np.float64]
        A dataclass containing the number of points, time array, and strain array.

    """
    initial_time = kwargs.get("initial_time", 0.0)
    unloading_period = kwargs.get("unloading_period", period)
    xp = np.add.accumulate(
        np.array(
            [
                initial_time,
                0.5 * period,
                duration,
                0.5 * unloading_period,
            ],
            dtype=np.float64,
        ),
    )
    yp = np.zeros(4, dtype=np.float64)
    yp[1:3] = max_strain
    nt = int((xp.max() - xp.min()) / dt) + 1
    time = np.linspace(xp.min(), xp.max(), nt, dtype=np.float64)
    return DataCurve(
        n=nt,
        time=time,
        strain=np.interp(time, xp, yp),
    )
