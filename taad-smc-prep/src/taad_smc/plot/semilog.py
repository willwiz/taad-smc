# Copyright (c) 2025 Will Zhang
# pyright: reportUnknownMemberType=false
from typing import TYPE_CHECKING, Unpack

import numpy as np
from matplotlib import pyplot as plt
from pytools.plotting.api import create_figure, legend_kwargs, style_kwargs, update_figure_setting

if TYPE_CHECKING:
    from collections.abc import Sequence
    from pathlib import Path

    from pytools.plotting.trait import PlotKwargs
    from taad_smc.plot.struct import PlotData


def semilogx[T: np.floating](
    data: Sequence[PlotData[T]],
    fout: Path,
    **kwargs: Unpack[PlotKwargs],
) -> None:
    fig, ax = create_figure(**kwargs)
    update_figure_setting(fig, **kwargs)
    style = style_kwargs(**kwargs)
    for d in data:
        ax.semilogx(d.x, d.y, **style)
    curve_labels = kwargs.get("curve_labels")
    if curve_labels is not None:
        fig.legend(curve_labels, **legend_kwargs(**kwargs))
    fig.savefig(fout)
    plt.close(fig)


def plotxy[T: np.floating](
    data: Sequence[PlotData[T]],
    fout: Path,
    **kwargs: Unpack[PlotKwargs],
) -> None:
    fig, ax = create_figure(**kwargs)
    update_figure_setting(fig, **kwargs)
    style = style_kwargs(**kwargs)
    for d in data:
        ax.plot(d.x, d.y, **style)
    curve_labels = kwargs.get("curve_labels")
    if curve_labels is not None:
        fig.legend(curve_labels, **legend_kwargs(**kwargs))
    fig.savefig(fout)
    plt.close(fig)
