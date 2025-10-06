# Copyright (c) 2023, Will Zhang
# All rights reserved.
# pyright: reportUnknownMemberType = false

from collections.abc import Sequence
from pathlib import Path
from typing import Unpack

import matplotlib.pyplot as plt
import numpy as np
from arraystubs import Arr1
from pytools.plotting.api import create_figure, style_kwargs, update_figure_setting
from pytools.plotting.trait import PlotKwargs

from ._structs import DataCurve


def plot_xvt[F: np.floating](
    data: Sequence[tuple[Arr1[F], Arr1[F]]],
    **kwargs: Unpack[PlotKwargs],
) -> None:
    fig, ax = create_figure(**kwargs)
    update_figure_setting(fig, **kwargs)
    ax_style = style_kwargs(**kwargs)
    for x, y in data:
        ax.plot(x, y, **ax_style)
    plt.close(fig)


def create_experimentprotocol_figure[F: np.floating](
    *data: DataCurve[F],
    fout: Path,
    **kwargs: Unpack[PlotKwargs],
) -> None:
    fig, ax = create_figure(**kwargs)
    update_figure_setting(fig, **kwargs)
    ax_style = style_kwargs(**kwargs)
    for curve in data:
        ax.plot(curve.time, curve.strain, **ax_style)
    fig.savefig(fout.with_suffix(".png"), transparent=True)
    plt.close(fig)
