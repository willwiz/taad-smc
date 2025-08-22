# Copyright (c) 2025 Will Zhang
import dataclasses as dc
import json
from pathlib import Path
from typing import Any

import numpy as np
from pytools.logging.trait import NULL_LOG, ILogger

from ._nptdms import import_tdms_muscle_typeless
from .struct import TDMSData, TDMSMetaData


def import_tdms_raw(file: Path) -> TDMSData[np.float64]:
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
    return import_tdms_muscle_typeless(file)


def export_tdms[F: np.floating](data: TDMSData[F], file: Path) -> None:
    with file.with_suffix(".json").open("w") as f:
        json.dump(dc.asdict(data.meta), f, indent=4)
    data_csv = np.column_stack((data.time, data.disp, data.force))
    np.savetxt(
        file.with_suffix(".raw"),
        data_csv,
        delimiter=",",
        header="Time,Position,Force",
        comments="",
    )


def read_tdms_metadata_from_json(raw: dict[str, Any], *, log: ILogger = NULL_LOG) -> TDMSMetaData:
    for field in dc.fields(TDMSMetaData):
        if raw.get(field.name) is None:
            log.error(f"Missing {field.name} in TDMS metadata.")
            raise ValueError
    return TDMSMetaData(**{k.name: raw[k.name] for k in dc.fields(TDMSMetaData)})


def import_tdms(file: Path) -> TDMSData[np.float64]:
    with file.with_suffix(".json").open("r") as f:
        data_dict = json.load(f)
        metadata = read_tdms_metadata_from_json(data_dict)
    data_csv = np.loadtxt(file.with_suffix(".raw"), delimiter=",", skiprows=1, dtype=np.float64)
    return TDMSData(
        time=data_csv[:, 0],
        disp=data_csv[:, 1],
        force=data_csv[:, 2],
        command=metadata.command,
        fiber_length=metadata.fiber,
        initial_force=metadata.force,
        initial_position=metadata.position,
        meta=metadata,
    )
