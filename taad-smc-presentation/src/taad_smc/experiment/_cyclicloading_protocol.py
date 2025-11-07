# pyright: reportUnknownMemberType = false
from typing import TYPE_CHECKING, TypedDict, Unpack

import numpy as np

from ._structs import DataCurve

if TYPE_CHECKING:
    from collections.abc import Sequence


class CyclicLoadingProtocolKwargs(TypedDict, total=False):
    initial_time: float


def cyclic_loading_protocol(
    max_strain: float,
    period: float,
    num_cycles: int,
    dt: float,
    **kwargs: Unpack[CyclicLoadingProtocolKwargs],
) -> DataCurve[np.float64]:
    """Generate a cyclic loading protocol data curve.

    Parameters
    ----------
    max_strain : float
        The maximum strain value.
    period : float
        The period of one cycle.
    num_cycles : int
        The number of cycles.
    dt : float
        The time step for the generated data.
    **kwargs : CyclicLoadingProtocolKwargs
        Additional keyword arguments.
        - initial_time : float, optional
            The initial time offset (default is 0.0).

    Returns
    -------
    DataCurve[np.float64]
        A dataclass containing the number of points, time array, and strain array.

    """
    initial_time = kwargs.get("initial_time", 0.0)
    xp = np.add.accumulate(
        np.array(
            [
                initial_time,
                *[0.5 * period for _ in range(num_cycles) for _ in range(2)],
            ],
            dtype=np.float64,
        ),
    )
    yp = np.zeros(2 * num_cycles + 1, dtype=np.float64)
    yp[1::2] = max_strain
    nt = int((xp.max() - xp.min()) / dt) + 1
    time = np.linspace(xp.min(), xp.max(), nt, dtype=np.float64)
    return DataCurve(
        n=nt,
        time=time,
        strain=np.interp(time, xp, yp),
    )


def create_cyclic_loading_experimentaldata(
    max_strain: float,
    period: float,
    num_cycles: int,
    dt: float,
) -> Sequence[DataCurve[np.float64]]:
    return [
        cyclic_loading_protocol(s * max_strain, s * period, num_cycles, dt, initial_time=t)
        for s, t in zip([1, 2 / 3, 1 / 3], [0, 3 * period, 5 * period], strict=True)
    ]
