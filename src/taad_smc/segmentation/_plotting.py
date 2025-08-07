# pyright: reportUnknownMemberType = false
from collections.abc import Sequence
from pathlib import Path

import numpy as np
from arraystubs import Arr1
from matplotlib import pyplot as plt
from pytools.plotting.api import create_figure, update_figure_setting

from taad_smc.segmentation.struct import DataSeries, Segmentation, Split


def plot_transition[F: np.floating, I: np.integer](
    data: DataSeries[F],
    nodes: Arr1[I],
    seg: Segmentation[I],
    splits: Sequence[Split],
    *,
    fout: Path,
) -> None:
    split_indicies = np.array([s.idx for s in splits], dtype=np.intp)
    i_start = (seg.idx[nodes.min()] + seg.idx[nodes.min() - 1]) // 2
    i_end = seg.idx[nodes.max() + 1]
    start = data.x[int(i_start)]
    end = data.x[min(int(i_end), len(data.x) - 1)]
    fig, ax = create_figure(4, figsize=(10, 8), dpi=180)
    update_figure_setting(fig)
    ax[0].set_xlim(start, end)
    ax[1].set_xlim(start, end)
    ax[2].set_xlim(start, end)
    ax[2].set_ylim(-1.2, 1.2)
    ax[3].set_xlim(start, end)
    ax[3].set_ylim(-1.2, 1.2)
    ax[0].plot(data.x, data.y, "k-", label="Displacement")
    ax[0].plot(data.x[split_indicies], data.y[split_indicies], "ro", label="Segments")
    ax[0].set_xlabel("Time (s)")
    ax[1].plot(data.x, data.z, "k-", label="Filtered")
    ax[1].plot(data.x[split_indicies], data.z[split_indicies], "ro", label="Segments")
    ax[1].set_xlabel("Time (s)")
    ax[2].plot(
        data.x,
        data.dz / data.dz[split_indicies[0] : split_indicies[-2]].max(),
        "k-",
        label="Slope",
    )
    ax[2].set_xlabel("Time (s)")
    ax[3].plot(
        data.x,
        data.ddz / data.ddz[split_indicies[0] : split_indicies[-2]].max(),
        "k-",
        label="Inflection",
    )
    ax[3].set_xlabel("Time (s)")
    fig.savefig(fout)
    plt.close(fig)
