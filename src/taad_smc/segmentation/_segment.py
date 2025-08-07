from collections.abc import Sequence
from pathlib import Path
from pprint import pformat

import numpy as np
from arraystubs import Arr1
from pytools.logging.trait import NULL_LOG, ILogger
from scipy.ndimage import gaussian_filter1d
from scipy.signal import find_peaks

from taad_smc.segmentation._plotting import plot_transition

from .struct import DataSeries, Segmentation, Split, TAADCurve
from .trait import CurvePoint


def filtered_derivatives[F: np.floating](
    time: Arr1[F],
    data: Arr1[F],
    *,
    smoothing_window: float,
) -> DataSeries[F]:
    x = gaussian_filter1d(data, smoothing_window)
    for _ in range(5):
        x = gaussian_filter1d(x, smoothing_window)
    dx = np.gradient(x)
    ddx = np.gradient(dx)
    return DataSeries(x=time, y=data, z=x, dz=dx, ddz=ddx)


def find_indexes[F: np.floating, I: np.integer](
    data: Arr1[F],
    nodes: Arr1[I],
    seg: Segmentation[I],
    *,
    log: ILogger = NULL_LOG,
) -> Sequence[Split]:
    i_start = (seg.idx[nodes.min()] + seg.idx[nodes.min() - 1]) // 2
    i_end = seg.idx[nodes.max() + 1]
    log.debug(
        "Finding indexes for nodes:",
        pformat(nodes, indent=2, sort_dicts=False),
        "with current indicies:",
        pformat(seg.idx[nodes], indent=2, sort_dicts=False),
        f"from {i_start} to {i_end}.",
    )
    relative_data = np.zeros_like(data)
    relative_data[i_start:i_end] = data[i_start:i_end] / data[seg.idx[nodes[0] : nodes[-2]]].max()
    peaks, _ = find_peaks(np.maximum(relative_data, 0), prominence=0.3, width=50)
    valleys, _ = find_peaks(np.maximum(-relative_data, 0), prominence=0.3, width=50)
    splits = [Split(int(idx), CurvePoint.PEAK) for idx in peaks] + [
        Split(int(idx), CurvePoint.VALLEY) for idx in valleys
    ]
    splits = sorted(splits, key=lambda x: x.idx)
    return [s for s in splits if i_start < s.idx <= i_end]


def validate_curve_indices[I: np.integer](
    seg: Segmentation[I],
    nodes: Arr1[I],
    splits: Sequence[Split],
    *,
    log: ILogger = NULL_LOG,
) -> Segmentation[I]:
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
    return Segmentation(idx=updated_indices, kind=seg.kind)


def segment_duration[F: np.floating, I: np.integer](
    data: DataSeries[F],
    curves: Sequence[TAADCurve[F, I]],
    seg: Segmentation[I],
    *,
    fout: Path,
    log: ILogger = NULL_LOG,
) -> Segmentation[I]:
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
    plot_transition(data, nodes, seg, splits, fout=fout)
    return validate_curve_indices(seg, nodes, splits, log=log)
