# Copyright (c) 2025 Will Zhang
# pyright: reportUnknownMemberType=false

import json
from pathlib import Path
from typing import TYPE_CHECKING

import pandas as pd
from pytools.result import Err, Ok
from taad_smc.tdms.api import import_tdms_data

from ._tools import construct_protocol, validate_protocol
from ._validation import JSON_DICT, is_all_test_protocols, is_specimen_info, is_test_protocol

if TYPE_CHECKING:
    from collections.abc import Mapping

    from .trait import SpecimenInfo, TestProtocol

__all__ = [
    "construct_protocol",
    "import_df",
    "import_specimen_info",
    "import_tdms_data",
    "import_test_protocol",
    "is_all_test_protocols",
    "is_specimen_info",
    "is_test_protocol",
    "validate_protocol",
]


def import_df(file: Path) -> Ok[pd.DataFrame] | Err:
    """Return a pandas DataFrame from a CSV file.

    Parameters
    ----------
    file : Path
        Path to the CSV file to read.

    Returns
    -------
    df : pd.DataFrame
        DataFrame containing the data from the CSV file.

    """
    if file.exists():
        return Ok(pd.read_csv(file))
    return Err(FileExistsError(f"{file} not found"))


# def _is_dict(dct: object) -> TypeIs[dict[Any, Any]]:
#     return isinstance(dct, dict)


# def _validate_specimen_info(dct: object) -> TypeIs[SpecimenInfo]:
#     if not _is_dict(dct):
#         return False
#     for key, value_type in get_type_hints(SpecimenInfo).items():
#         value = dct.get(key)
#         if value is None:
#             print(f"Missing key: {key}")
#             return False
#         if get_origin(value_type) is Literal:
#             if value not in get_args(value_type):
#                 print(f"Invalid value for key: {key}.")
#                 print(f"Expected one of {get_args(value_type)}, got {value}")
#                 return False
#         elif not isinstance(value, value_type):
#             print(f"Invalid type for key: {key}.")
#             print(f"Expected {value_type}, got {type(value)}")
#             return False
#     return True


def import_specimen_info(file: Path | str) -> Ok[SpecimenInfo] | Err:
    file = Path(file)
    info_file = file.parent / "key.json"
    if not info_file.exists():
        msg = f"File {info_file} does not exist."
        return Err(FileExistsError(msg))
    with info_file.open("r") as f:
        info: JSON_DICT = json.load(f)
    if is_specimen_info(info):
        return Ok(info)
    msg = f"Specimen info in {info_file} is invalid."
    return Err(ValueError(msg))


def import_test_protocol(file: Path) -> Ok[Mapping[str, TestProtocol]] | Err:
    if not file.exists():
        msg = f"File {file} does not exist."
        return Err(FileExistsError(msg))
    with file.open("r") as f:
        meta_data = json.load(f)
    if is_all_test_protocols(meta_data):
        return Ok(meta_data)
    return Err(ValueError(f"Test protocol in {file} is invalid."))
