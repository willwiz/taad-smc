# Copyright (c) 2025 Will Zhang
from pprint import pformat
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
from pytools.logging.api import NLOGGER
from pytools.result import Err, Ok
from taad_smc.io.api import import_specimen_info, import_tdms_data, import_test_protocol

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from pytools.logging.trait import ILogger
    from taad_smc.io.types import SpecimenInfo, TestProtocol
    from taad_smc.tdms.struct import TDMSData

    from pwlsplit.trait import Segmentation

    from ._types import FileNames


def _format_dict(dct: object, indent: int = 2) -> str:
    return pformat(dct, indent=indent, sort_dicts=False)


def import_data(
    names: FileNames,
    *,
    log: ILogger = NLOGGER,
) -> Ok[tuple[TDMSData[np.float64], Mapping[str, TestProtocol], SpecimenInfo]] | Err:
    match import_tdms_data(names.raw):
        case Ok(data):
            log.debug("TDMS data imported successfully.", _format_dict(data))
        case Err(e):
            return Err(e)
    match import_test_protocol(names.protocol):
        case Ok(protocol):
            log.debug("Test protocol imported successfully.", _format_dict(protocol))
        case Err(e):
            return Err(e)
    match import_specimen_info(names.info):
        case Ok(info):
            log.debug("Specimen info imported successfully.", _format_dict(info))
        case Err(e):
            return Err(e)
    return Ok((data, protocol, info))


def construct_postprocessed_df[F: np.floating, I: np.integer](
    data: TDMSData[F],
    index: Segmentation[F, I],
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
            "disp": data.disp - data.disp[0],
            "force": data.force,
        },
    )
