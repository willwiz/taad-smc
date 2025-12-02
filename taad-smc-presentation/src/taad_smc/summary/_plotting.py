# Copyright (c) 2025 Will Zhang
# pyright: reportUnknownMemberType=false
from typing import TYPE_CHECKING, Unpack

import numpy as np
from matplotlib import pyplot as plt
from pytools.plotting.api import create_figure, legend_kwargs, style_kwargs, update_figure_setting

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence
    from pathlib import Path

    from matplotlib.axes import Axes
    from matplotlib.figure import Figure
    from pytools.plotting.trait import PlotKwargs

    from ._types import PlotData


def create_ppgrid(**kwargs: Unpack[PlotKwargs]) -> tuple[Figure, Sequence[Sequence[Axes]]]:
    fig_kwargs: PlotKwargs = {"figsize": (16, 9)}
    fig, axes = create_figure(nrows=3, ncols=4, **(fig_kwargs | kwargs))
    update_figure_setting(fig, **kwargs)
    return fig, axes


def save_and_close_fig(fig: Figure, fout: Path, **kwargs: Unpack[PlotKwargs]) -> None:
    fig.savefig(fout, dpi=kwargs.get("dpi", 300), transparent=kwargs.get("transparent", False))
    plt.close(fig)


def semilogx_on_axis[T: np.number](
    data: Iterable[PlotData[T]],
    ax: Axes,
    **kwargs: Unpack[PlotKwargs],
) -> None:
    style = style_kwargs(**kwargs)
    for d in data:
        ax.semilogx(d.x, d.y, **style)
    curve_labels = kwargs.get("curve_labels")
    if curve_labels is not None:
        ax.legend(curve_labels, **legend_kwargs(**kwargs))


def plotxy_on_axis[T: np.number](
    data: Iterable[PlotData[T]],
    ax: Axes,
    **kwargs: Unpack[PlotKwargs],
) -> None:
    style = style_kwargs(**kwargs)
    for d in data:
        ax.plot(d.x, d.y, **style)
    curve_labels = kwargs.get("curve_labels")
    if curve_labels is not None:
        ax.legend(curve_labels, **legend_kwargs(**kwargs))
