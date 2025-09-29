# Copyright (c) 2025 Will Zhang
# License: MIT License
# pyright: reportUnknownMemberType=false
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from pytools.plotting.api import create_figure, update_figure_setting

from .struct import TDMSData


def plot_data[F: np.floating](data: TDMSData[F], *, fout: Path) -> None:
    fig, ax = create_figure(2, figsize=(8, 3), dpi=180)
    update_figure_setting(fig, padleft=0.2, padbottom=0.15)
    # indices = data.time > 600.0
    # time = data.time[indices] - 600.0
    # disp = data.disp[indices]
    # force = data.force[indices]
    # ax[0].plot(time, force, "k-", label="Force (mN)")
    # ax[0].set_xlabel("Time (s)")
    # ax[0].set_ylabel("Force (mN)")
    # ax[1].plot(time, force, "k-", label="Force (mN)")
    # ax[0].plot(time, disp, "k-", label="Strain")
    ax[0].plot(data.time, data.disp, "k-", label="Strain")
    ax[0].set_xlabel("Time (s)")
    ax[0].set_ylabel("Strain")
    ax[1].plot(data.time, data.force, "k-", label="Force (mN)")
    ax[1].set_xlabel("Time (s)")
    ax[1].set_ylabel("Force (mN)")
    fig.savefig(fout)
    plt.close(fig)
