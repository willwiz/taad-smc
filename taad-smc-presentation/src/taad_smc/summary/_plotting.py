# Copyright (c) 2025 Will Zhang
# pyright: reportUnknownMemberType=false
from typing import TYPE_CHECKING, Unpack

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from pytools.plotting.api import (
    create_figure,
    legend_kwargs,
    style_kwargs,
    update_axis_setting,
    update_figure_setting,
)
from pytools.plotting.trait import BarPlotKwargs, PlotKwargs

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping, Sequence
    from pathlib import Path

    from matplotlib.axes import Axes
    from matplotlib.figure import Figure

    from ._types import PlotData


def create_ppgrid(**kwargs: Unpack[PlotKwargs]) -> tuple[Figure, Sequence[Sequence[Axes]]]:
    fig_kwargs = (
        PlotKwargs(
            figsize=(16, 10),
            padbottom=0.20,
            padleft=0.20,
            padright=0.03,
            padtop=0.15,
            head_space=0.10,
        )
        | kwargs
    )
    fig, axes = create_figure(nrows=3, ncols=4, **fig_kwargs)
    update_figure_setting(fig, **fig_kwargs)
    axes[0][0].axis("off")
    title = kwargs.get("title")
    if title:
        fig.suptitle(title, fontsize=20)
    return fig, axes


def save_and_close_fig(fig: Figure, fout: Path, **kwargs: Unpack[PlotKwargs]) -> None:
    fig.savefig(fout, dpi=kwargs.get("dpi", 300), transparent=kwargs.get("transparent", False))
    plt.close(fig)


def semilogx_on_axis[T: np.number](
    data: Iterable[PlotData[T]],
    ax: Axes,
    **kwargs: Unpack[PlotKwargs],
) -> None:
    update_axis_setting(ax, **kwargs)
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
    update_axis_setting(ax, **kwargs)
    style = style_kwargs(**kwargs)
    for d in data:
        ax.plot(d.x, d.y, **style)
    curve_labels = kwargs.get("curve_labels")
    if curve_labels is not None:
        ax.legend(curve_labels, **legend_kwargs(**kwargs))


def grouped_bar_on_axis(
    data: Mapping[str, Mapping[str, float]],
    ax: Axes,
    bar_color: Mapping[str, str] | None = None,
    fill_color: Mapping[str, str] | None = None,
    hatches: Mapping[str, str] | None = None,
    **kwargs: Unpack[PlotKwargs],
) -> None:
    update_axis_setting(ax, **kwargs)
    n_groups = len(data)
    n_bar_group = max(len(v) for v in data.values())
    bar_width = 1.0 / (n_groups + 1)
    x = np.arange(n_bar_group)
    offset = 0.0
    plot_kwargs = BarPlotKwargs(width=bar_width, linewidth=3)
    if bar_color is not None:
        plot_kwargs = plot_kwargs | BarPlotKwargs(
            edgecolor=[bar_color[k] for k in next(iter(data.values()))]
        )
    for r, d in data.items():
        offset = offset + bar_width
        if hatches is not None:
            plot_kwargs = plot_kwargs | BarPlotKwargs(hatch=hatches[r])
        if fill_color is not None:
            plot_kwargs = plot_kwargs | BarPlotKwargs(color=fill_color[r])
        ax.bar(
            x + offset,
            list(d.values()),
            **plot_kwargs,
        )
    ax.set_xticks(x + bar_width * n_bar_group / 2)
    ax.set_xticklabels([str(x) for x in next(iter(data.values()))])


def create_legend_on_axis(ax: Axes) -> None:
    custom_lines = [
        Line2D([0], [0], color="k", lw=1),
        Line2D([0], [0], color="r", lw=1),
        Line2D([0], [0], color="b", lw=1),
        Line2D([0], [0], color="k", lw=1),
        Line2D([0], [0], color="b", lw=1),
        Line2D([0], [0], color="orange", lw=1),
    ]
    activation_legend = ax.legend(
        custom_lines,
        ["Fresh", "Activated", "Deactivated", "30%", "20%", "10%"],
        ncols=2,
        fontsize=13,
        loc="upper left",
    )
    ax.add_artist(activation_legend)
    ax.legend(
        [
            Line2D([0], [0], color="k", ls="-", lw=1),
            Line2D([0], [0], color="k", ls="--", lw=1),
            Line2D([0], [0], color="k", ls=":", lw=1),
            Patch(facecolor="gray", edgecolor="k", lw=1),
            Patch(facecolor="none", hatch="x", edgecolor="k", lw=1),
            Patch(facecolor="none", hatch=".", edgecolor="k", lw=1),
        ],
        ["", "", "", "Fast", "Mid", "Slow"],
        ncols=2,
        fontsize=13,
        loc="lower left",
    )
