# Copyright (c) 2025 Will Zhang
# pyright: reportUnknownMemberType=false

import json
from pathlib import Path
from typing import Any, Literal, TypeIs, get_args, get_origin, get_type_hints

from pytools.result import Err, Ok

from ._types import SpecimenInfo


def _is_dict(dct: object) -> TypeIs[dict[Any, Any]]:
    return isinstance(dct, dict)


def valid_specimen_info(dct: object) -> TypeIs[SpecimenInfo]:
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
    if valid_specimen_info(info):
        return Ok(info)
    msg = f"Specimen info in {info_file} is invalid."
    return Err(ValueError(msg))
