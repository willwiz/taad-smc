# pyright: reportUnknownMemberType=false
from collections.abc import Sequence
from pathlib import Path
from typing import Unpack

import numpy as np
from matplotlib import pyplot as plt
from pytools.plotting.api import create_figure, figstyle, legend_kwargs, update_figure_setting
from pytools.plotting.trait import PlotKwargs

from taad_smc.plotting.struct import PlotData


def semilogx[T: np.number](
    data: Sequence[PlotData[T]],
    fout: Path,
    **kwargs: Unpack[PlotKwargs],
) -> None:
    fig, ax = create_figure(**kwargs)
    update_figure_setting(fig, **kwargs)
    style = figstyle(**kwargs)
    for d in data:
        ax.semilogx(d.x, d.y, **style)
    curve_labels = kwargs.get("curve_labels")
    if curve_labels is not None:
        fig.legend(curve_labels, **legend_kwargs(**kwargs))
    fig.savefig(fout)
    plt.close(fig)


def plotxy[T: np.number](
    data: Sequence[PlotData[T]],
    fout: Path,
    **kwargs: Unpack[PlotKwargs],
) -> None:
    fig, ax = create_figure(**kwargs)
    update_figure_setting(fig, **kwargs)
    style = figstyle(**kwargs)
    for d in data:
        ax.plot(d.x, d.y, **style)
    curve_labels = kwargs.get("curve_labels")
    if curve_labels is not None:
        fig.legend(curve_labels, **legend_kwargs(**kwargs))
    fig.savefig(fout)
    plt.close(fig)
