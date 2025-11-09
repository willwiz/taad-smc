# Copyright (c) 2025 Will Zhang
import json
from pathlib import Path
from pprint import pformat
from typing import TYPE_CHECKING, Any, Literal, TypeIs, get_args, get_origin, get_type_hints

import numpy as np
import pandas as pd
from pytools.logging.api import NLOGGER
from pytools.result import Err, Ok
from taad_smc.segment.trait import SpecimenInfo, TestProtocol
from taad_smc.tdms.api import import_tdms_data

from pwlsplit.trait import Segmentation

from ._trait import FileNames

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from pytools.logging.trait import ILogger
    from taad_smc.tdms.struct import TDMSData


def import_test_protocol(file: Path) -> Ok[Mapping[str, TestProtocol]] | Err:
    if not file.exists():
        msg = f"File {file} does not exist."
        return Err(FileExistsError(msg))
    with file.open("r") as f:
        meta_data: dict[str, TestProtocol] = json.load(f)
    return Ok(meta_data)


def is_dict(dct: object) -> TypeIs[dict[Any, Any]]:
    return isinstance(dct, dict)


def validate_specimen_info(dct: object) -> TypeIs[SpecimenInfo]:
    if not is_dict(dct):
        return False
    for key, value_type in get_type_hints(SpecimenInfo).items():
        value = dct.get(key)
        if value is None:
            print(f"Missing key: {key}")
            return False
        if get_origin(value_type) is Literal:
            if value not in get_args(value_type):
                print(f"Invalid value for key: {key}.")
                print(f"Expected one of {get_args(value_type)}, got {value}")
                return False
        elif not isinstance(value, value_type):
            print(f"Invalid type for key: {key}.")
            print(f"Expected {value_type}, got {type(value)}")
            return False
    return True


def import_specimen_info(file: Path | str) -> Ok[SpecimenInfo] | Err:
    file = Path(file)
    info_file = file.parent / "key.json"
    if not info_file.exists():
        msg = f"File {info_file} does not exist."
        return Err(FileExistsError(msg))
    with info_file.open("r") as f:
        info = json.load(f)
    if not validate_specimen_info(info):
        msg = f"Specimen info in {info_file} is invalid."
        return Err(ValueError(msg))
    return Ok(info)


def import_data(
    names: FileNames,
    *,
    log: ILogger = NLOGGER,
) -> Ok[tuple[TDMSData[np.float64], Mapping[str, TestProtocol], SpecimenInfo]] | Err:
    match import_tdms_data(names.raw):
        case Ok(data):
            log.debug(
                "TDMS data imported successfully.",
                pformat(data, indent=2, sort_dicts=False),
            )
        case Err(e):
            return Err(e)
    match import_test_protocol(names.protocol):
        case Ok(protocol):
            log.debug(
                "Test protocol imported successfully.",
                pformat(protocol, indent=2, sort_dicts=False),
            )
        case Err(e):
            return Err(e)
    match import_specimen_info(names.info):
        case Ok(info):
            log.debug(
                "Specimen info imported successfully.",
                pformat(info, indent=2, sort_dicts=False),
            )
        case Err(e):
            return Err(e)
    return Ok((data, protocol, info))


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
            "disp": data.disp - data.disp[0],
            "force": data.force,
        },
    )
