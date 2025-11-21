from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
from pytools.logging.trait import LogLevel
from pytools.result import Err, Ok
from scipy.ndimage import gaussian_filter
from taad_smc.io.api import construct_protocol

from pwlsplit.trait import PreppedData, Segmentation, SegmentDict

from ._trait import PROTOCOL_MAP, FileNames, SegmentOptions

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence
    from pathlib import Path

    from pytools.arrays import A1
    from taad_smc.io.trait import SpecimenInfo, TestProtocol
    from taad_smc.tdms.struct import TDMSData

    from ._argparse import ParsedArguments


def parser_optional_args(args: ParsedArguments) -> SegmentOptions:
    return SegmentOptions(
        plot=args.plot,
        overwrite=args.overwrite,
        log=LogLevel[args.log],
        window=args.smoothing_window,
        repeat=args.smoothing_repeat,
    )


def create_names(file: Path) -> Ok[FileNames] | Err:
    parent = file.parent
    if not (parent / "protocol.json").exists():
        return Err(FileExistsError(f"File {parent / 'protocol.json'} does not exist."))
    if not (parent / "key.json").exists():
        return Err(FileExistsError(f"File {parent / 'key.json'} does not exist."))
    return Ok(
        FileNames(
            parent=parent,
            raw=file,
            csv=file.with_suffix(".csv"),
            protocol=parent / "protocol.json",
            info=parent / "key.json",
        )
    )


def filter_derivative[F: np.floating](
    arr: A1[F], *, window: float, repeat: int = 5
) -> PreppedData[F]:
    y: A1[F] = arr - arr[0]
    for _ in range(repeat):
        y = gaussian_filter(y, sigma=window)
    # y = signal.wiener(y, mysize=int(window)).astype(arr.dtype)
    dy = np.gradient(y)
    for _ in range(repeat):
        dy = gaussian_filter(dy, sigma=window)
    ddy = np.gradient(dy)
    for _ in range(repeat):
        ddy = gaussian_filter(ddy, sigma=window)
    return PreppedData(n=len(arr), x=arr, y=y, dy=dy / dy.max(), ddy=ddy / ddy.max())


def compile_taadsmc_curves(
    protocol: Mapping[str, TestProtocol],
) -> Ok[tuple[PROTOCOL_MAP, Sequence[SegmentDict]]] | Err:
    compiled_curves = {prot: construct_protocol(test) for prot, test in protocol.items()}
    failed = [p for p, c in compiled_curves.items() if isinstance(c, Err)]
    if failed:
        msg = f"Failed to construct protocol for: \n {failed}"
        return Err(LookupError(msg))
    unwrapped_protocol = {
        p: dict(curves.val.items())
        for p, curves in compiled_curves.items()
        if isinstance(curves, Ok)
    }
    k = 0
    protocol_map = {
        p: {c: {(k := k + 1): s for s in segments} for c, segments in cycles.items()}
        for p, cycles in unwrapped_protocol.items()
    }
    curves = [
        s
        for cycles in unwrapped_protocol.values()
        for segments in cycles.values()
        for s in segments
    ]
    return Ok((protocol_map, curves))


def construct_postprocessed_df[F: np.floating, I: np.integer](
    data: TDMSData[F],
    info: SpecimenInfo,
    protocol_map: PROTOCOL_MAP,
    index: Segmentation[F, I],
) -> pd.DataFrame:
    protocols = np.empty_like(data.time, dtype="U20")
    cycle = np.empty_like(data.time, dtype="U20")
    mode = np.empty_like(data.time, dtype="U20")
    for p, cycles in protocol_map.items():
        for c, segments in cycles.items():
            for ix, seg in segments.items():
                slice_ix = slice(index.idx[ix - 1], index.idx[ix])
                protocols[slice_ix] = p.encode("utf-8")
                cycle[slice_ix] = c.encode("utf-8")
                mode[slice_ix] = seg["curve"].encode("utf-8")
    disp = (data.disp + 0.5 * info["strain"]) * info["input_length_mm"] / info["actual_length_mm"]
    return pd.DataFrame(
        {
            "protocol": protocols,
            "cycle": cycle,
            "mode": mode,
            "time": data.time,
            "disp": disp,
            "force": data.force,
        },
    )
