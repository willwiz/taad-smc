from pprint import pformat
from typing import TYPE_CHECKING

import numpy as np
from pytools.logging.api import NLOGGER
from scipy.ndimage import gaussian_filter1d
from scipy.signal import find_peaks

from ._plotting import plot_transition
from .struct import DataSeries, Segmentation, Split, TAADCurve
from .trait import CurvePoint

if TYPE_CHECKING:
    from collections.abc import Sequence
    from pathlib import Path

    from pytools.arrays import A1
    from pytools.logging.trait import ILogger


def filtered_derivatives[F: np.floating](
    time: A1[F],
    data: A1[F],
    *,
    smoothing_window: float,
    repeat: int = 5,
) -> DataSeries[F]:
    # sos = butter(15, 100, "lowpass", fs=5000, output="sos")
    x = data.copy()
    # x = sosfiltfilt(sos, x).astype(data.dtype)
    x = gaussian_filter1d(x, smoothing_window)
    for _ in range(repeat):
        x = gaussian_filter1d(x, smoothing_window)
    dx: A1[F] = np.gradient(x) * 5000
    # dx = sosfiltfilt(sos, dx).astype(data.dtype)
    # for _ in range(repeat):
    #     dx = gaussian_filter1d(dx, 3)
    ddx: A1[F] = np.gradient(dx)
    # ddx = sosfiltfilt(sos, ddx).astype(data.dtype)
    for _ in range(repeat):
        ddx = gaussian_filter1d(ddx, 10)
    ddx = ddx / ddx.max()
    # dx = sosfilt(sos, dx).astype(data.dtype)
    # ddx = sosfilt(sos, ddx).astype(data.dtype)
    return DataSeries(x=time, y=data, z=x, dz=dx, ddz=ddx)


def find_indexes[F: np.floating, I: np.integer](
    data: A1[F],
    nodes: A1[I],
    seg: Segmentation[I, F],
    *,
    log: ILogger = NLOGGER,
) -> Sequence[Split]:
    i_start = (seg.idx[nodes.min()] + seg.idx[nodes.min() - 1]) // 2
    i_end = seg.idx[-1]
    log.debug(
        "Finding indexes for nodes:",
        pformat(nodes, indent=2, sort_dicts=False),
        "with current indicies:",
        pformat(seg.idx[nodes], indent=2, sort_dicts=False),
        f"from {i_start} to {i_end}.",
    )
    rates = np.absolute(seg.rate[nodes]).min()
    relative_data = np.zeros_like(data)
    relative_data[i_start:] = data[i_start:] / rates
    print("max relative data is :", relative_data[i_start:i_end].max())
    peaks, _ = find_peaks(np.maximum(relative_data, 0), prominence=0.2, height=0.1)
    valleys, _ = find_peaks(np.maximum(-relative_data, 0), prominence=0.2, height=0.1)
    splits = [Split(int(idx), CurvePoint.PEAK) for idx in peaks] + [
        Split(int(idx), CurvePoint.VALLEY) for idx in valleys
    ]
    splits = sorted(splits, key=lambda x: x.idx)
    return [s for s in splits if i_start < s.idx]


def validate_curve_indices[I: np.integer, F: np.floating](
    seg: Segmentation[I, F],
    nodes: A1[I],
    splits: Sequence[Split],
    *,
    log: ILogger = NLOGGER,
) -> Segmentation[I, F]:
    if len(splits) < len(nodes):
        msg = f"Fewer splits ({len(splits)}) than expected ({len(nodes)})."
        log.warn(msg)
    j = 0
    updated_indices = seg.idx.copy()
    for i in nodes:
        for k in range(j, len(splits)):
            if seg.kind[int(i)] == splits[k].kind:
                break
        else:
            msg = (
                f"Could not find matching split for node {i} ({seg.kind[int(i)]})."
                f" Last split kind: {splits[-1].kind}."
            )
            log.error(
                msg,
                pformat(splits, indent=2, sort_dicts=False),
                pformat([seg.kind[int(i)] for i in nodes], indent=2, sort_dicts=False),
            )
            raise ValueError(msg)
        updated_indices[int(i)] = splits[k].idx
        j = k + 1
    log.debug(
        "Updated indices:",
        pformat(updated_indices[nodes], indent=2, sort_dicts=False),
        "Original indices:",
        pformat(seg.idx[nodes], indent=2, sort_dicts=False),
    )
    remainder = seg.idx[nodes.max() + 1 :] - seg.idx[nodes.max()]
    updated_indices[nodes.max() + 1 :] = remainder + updated_indices[nodes.max()]
    return Segmentation(idx=updated_indices, kind=seg.kind, rate=seg.rate)


def segment_duration[F: np.floating, I: np.integer](
    data: DataSeries[F],
    curves: Sequence[TAADCurve[F, I]],
    seg: Segmentation[I, F],
    *,
    fout: Path | None = None,
    log: ILogger = NLOGGER,
) -> Segmentation[I, F]:
    nodes = np.unique([i for c in curves for i in c.order])
    splits = find_indexes(data.ddz, nodes, seg, log=log)
    log.debug(
        "Splits found:",
        pformat(splits, indent=2, sort_dicts=False),
        "Splits expected:",
        pformat(
            [Split(seg.idx[int(i)], seg.kind[int(i)]) for i in nodes],
            indent=2,
            sort_dicts=False,
        ),
    )
    if fout is not None:
        plot_transition(data, nodes, seg, splits, fout=fout)
    seg = validate_curve_indices(seg, nodes, splits, log=log)
    seg.idx[-1] = len(data.x)
    return seg
