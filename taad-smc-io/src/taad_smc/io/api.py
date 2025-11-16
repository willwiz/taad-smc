# Copyright (c) 2025 Will Zhang
# pyright: reportUnknownMemberType=false

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, TypeIs, get_args, get_origin, get_type_hints

import pandas as pd
from pytools.result import Err, Ok
from taad_smc.tdms.api import import_tdms_data

from ._tools import construct_protocol, validate_protocol
from .trait import SpecimenInfo, TestProtocol

if TYPE_CHECKING:
    from collections.abc import Mapping

__all__ = [
    "construct_protocol",
    "import_df",
    "import_specimen_info",
    "import_tdms_data",
    "import_test_protocol",
    "validate_protocol",
]


def import_df(file: Path) -> pd.DataFrame:
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
    return pd.read_csv(file)


def _is_dict(dct: object) -> TypeIs[dict[Any, Any]]:
    return isinstance(dct, dict)


def _validate_specimen_info(dct: object) -> TypeIs[SpecimenInfo]:
    if not _is_dict(dct):
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
    if not _validate_specimen_info(info):
        msg = f"Specimen info in {info_file} is invalid."
        return Err(ValueError(msg))
    return Ok(info)


def import_test_protocol(file: Path) -> Ok[Mapping[str, TestProtocol]] | Err:
    if not file.exists():
        msg = f"File {file} does not exist."
        return Err(FileExistsError(msg))
    with file.open("r") as f:
        meta_data: dict[str, TestProtocol] = json.load(f)
    return Ok(meta_data)
