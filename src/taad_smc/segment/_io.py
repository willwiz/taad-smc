# Copyright (c) 2025 Will Zhang
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from pprint import pformat

import numpy as np
import pandas as pd
from pytools.logging.trait import NULL_LOG, ILogger

from taad_smc.struct import Error
from taad_smc.tdms.api import import_tdms, import_tdms_raw
from taad_smc.tdms.struct import TDMSData

from .struct import Segmentation
from .trait import TestProtocol


def import_test_protocol(file: Path) -> Mapping[str, TestProtocol] | Error:
    meta_data_file = file.parent / "protocol.json"
    if not meta_data_file.exists():
        msg = f"File {meta_data_file} does not exist."
        return Error(msg)
    with meta_data_file.open("r") as f:
        meta_data: dict[str, TestProtocol] = json.load(f)
    return meta_data


def import_data(
    file: Path,
    *,
    log: ILogger = NULL_LOG,
) -> tuple[TDMSData[np.float64], Mapping[str, TestProtocol]]:
    match file.suffix:
        case ".raw":
            data = import_tdms_raw(file)
        case ".tdms":
            data = import_tdms(file)
        case _:
            log.error(f"Unsupported file type: {file.suffix}")
            raise ValueError
    match data:
        case Error(msg=msg, trace=trace):
            log.error(trace.format())
            log.error(msg)
            raise ValueError
        case TDMSData():
            log.debug("TDMS data imported successfully.", pformat(data, indent=2, sort_dicts=False))
    protocol = import_test_protocol(file)
    match protocol:
        case Error(msg=msg, trace=trace):
            log.error(trace.format())
            log.error(msg)
            raise ValueError
        case _:
            log.debug(
                "Test protocol imported successfully.",
                pformat(protocol, indent=2, sort_dicts=False),
            )
    return data, protocol


def construct_postprocessed_df[F: np.floating, I: np.integer](
    data: TDMSData[F],
    index: Segmentation[I, F],
    tags: Sequence[tuple[str, int, str]],
) -> pd.DataFrame:
    protocols = np.empty(len(data.time), dtype="U20")
    cycle = np.zeros_like(data.time, dtype=np.intp)
    mode = np.empty(len(data.time), dtype="U20")
    for k, start, end in zip(tags, index.idx, index.idx[1:], strict=False):
        protocols[start:end] = k[0].encode("utf-8")
        cycle[start:end] = k[1]
        mode[start:end] = k[2].encode("utf-8")
    return pd.DataFrame(
        {
            "protocol": protocols,
            "cycle": cycle,
            "mode": mode,
            "time": data.time,
            "disp": data.disp,
            "force": data.force,
        },
    )
