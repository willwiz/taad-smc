# Copyright (c) 2025 Will Zhang
import dataclasses as dc
import json
from typing import TYPE_CHECKING, Any

import numpy as np
from pytools.result import Err, Ok

from ._nptdms import import_tdms_muscle_typeless
from .struct import TDMSData, TDMSMetaData

if TYPE_CHECKING:
    from pathlib import Path


__all__ = [
    "export_tdms",
    "import_tdms_raw",
]


def read_tdms_metadata_from_json(raw: dict[str, Any]) -> Ok[TDMSMetaData] | Err:
    for field in dc.fields(TDMSMetaData):
        if raw.get(field.name) is None:
            msg = f"Missing field {field.name} in TDMS metadata."
            return Err(ValueError(msg))
    return Ok(TDMSMetaData(**{k.name: raw[k.name] for k in dc.fields(TDMSMetaData)}))


def import_tdms_raw(file: Path) -> Ok[TDMSData[np.float64]] | Err:
    if file.suffix != ".raw":
        msg = f"Unsupported file type: {file.suffix}"
        return Err(ValueError(msg))
    if not file.exists():
        msg = f"File {file} does not exist."
        return Err(FileExistsError(msg))
    if not file.with_suffix(".json").exists():
        msg = f"File {file.with_suffix('.json')} does not exist."
        return Err(FileExistsError(msg))
    with file.with_suffix(".json").open("r") as f:
        data_dict = json.load(f)
        match read_tdms_metadata_from_json(data_dict):
            case Err(e):
                return Err(e)
            case Ok(metadata):
                pass
    data_csv = np.loadtxt(file, delimiter=",", skiprows=1, dtype=np.float64)
    return Ok(
        TDMSData(
            time=data_csv[:, 0],
            disp=data_csv[:, 1],
            force=data_csv[:, 2],
            command=metadata.command,
            fiber_length=metadata.fiber,
            initial_force=metadata.force,
            initial_position=metadata.position,
            meta=metadata,
        )
    )


def export_tdms[F: np.floating](data: TDMSData[F], *, prefix: Path) -> None:
    """Return None.

    Export the TDMS data to JSON and raw formats.

    Parameters
    ----------
    data : TDMSData[F]
        The TDMS data to export.
    prefix : Path, Kwarg
        The prefix for the output files.

    """
    with prefix.with_suffix(".json").open("w") as f:
        json.dump(dc.asdict(data.meta), f, indent=4)
    data_csv = np.column_stack((data.time, data.disp, data.force))
    np.savetxt(
        prefix.with_suffix(".raw"),
        data_csv,
        delimiter=",",
        header="Time,Position,Force",
        comments="",
    )


def import_tdms_data(file: Path) -> Ok[TDMSData[np.float64]] | Err:
    """Return struct containing the tdms data as numpy arrays.

    Parameters
    ----------
    file : Path
        Path to the TDMS file to read.

    Returns
    -------
    TDMSData[np.float64]
        Struct containing the TDMS data as numpy arrays.

    Note:
    This function is a wrapper around `import_tdms_muscle_typeless` and is
    provided for compatibility with typed function signatures.

    """
    match import_tdms_muscle_typeless(file):
        case Ok(data):
            return Ok(data)
        case Err(e):
            msg = f"Failed to import TDMS file {file}: {e}"
    match import_tdms_raw(file):
        case Ok(data):
            return Ok(data)
        case Err(e):
            msg = msg + f";\n {e}"
            return Err(ValueError(msg))
