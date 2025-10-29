# Copyright (c) 2023, Will Zhang
# All rights reserved.
# pyright: reportUnknownMemberType = false

from typing import TYPE_CHECKING, Unpack

import matplotlib.pyplot as plt
import numpy as np
from pytools.plotting.api import create_figure, style_kwargs, update_figure_setting

if TYPE_CHECKING:
    from collections.abc import Sequence

    from arraystubs import Arr1
    from pytools.plotting.trait import PlotKwargs


def plot_xvt[F: np.floating](
    data: Sequence[tuple[Arr1[F], Arr1[F]]],
    **kwargs: Unpack[PlotKwargs],
) -> None:
    fig, ax = create_figure(**kwargs)
    update_figure_setting(fig, **kwargs)
    ax_style = style_kwargs(**kwargs)
    ax_style = style_kwargs(**kwargs)
    for x, y in data:
        ax.plot(x, y, **ax_style)
    plt.close(fig)
