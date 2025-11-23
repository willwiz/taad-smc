import dataclasses as dc
import re
from typing import TYPE_CHECKING, Literal

import numpy as np
from pytools.result import Err, Ok
from taad_smc.io.api import import_df

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path

    import pandas as pd
    from pytools.arrays import A1


__all__ = [
    "PROTOCOLS",
    "PROTOCOL_NAMES",
    "PlotData",
    "SpecimenData",
]


@dc.dataclass(slots=True)
class PlotData[F: np.number]:
    x: A1[F]
    y: A1[F]


PROTOCOL_NAMES = Literal[
    "activation",
    "activated",
    "deactivation",
    "deactivated",
    "initial",
    "preconditioning_start",
    "preconditioning_activated",
    "preconditioning_deactivated",
    "rest_start",
    "rest_end",
]

PROTOCOLS: Mapping[PROTOCOL_NAMES, re.Pattern[str]] = {
    "activation": re.compile(r"activation_(?P<it>\d+)", re.IGNORECASE),
    "activated": re.compile(r"activated_(?P<it>\d+)", re.IGNORECASE),
    "deactivation": re.compile(r"deactivation_(?P<it>\d+)", re.IGNORECASE),
    "deactivated": re.compile(r"deactivated_(?P<it>\d+)", re.IGNORECASE),
    "initial": re.compile(r"initial_(?P<it>\d+)", re.IGNORECASE),
    "preconditioning_start": re.compile(r"preconditioning_start", re.IGNORECASE),
    "preconditioning_activated": re.compile(r"preconditioning_activated", re.IGNORECASE),
    "preconditioning_deactivated": re.compile(r"preconditioning_deactivated", re.IGNORECASE),
    "rest_start": re.compile(r"rest_start", re.IGNORECASE),
    "rest_end": re.compile(r"rest_end", re.IGNORECASE),
}


class CachableData:
    __slots__ = ("_data", "_file")
    _file: Path
    _data: pd.DataFrame | None

    def __init__(self, file: Path) -> None:
        self._file = file
        self._data = None

    @property
    def file(self) -> Path:
        return self._file

    def v(self) -> Ok[pd.DataFrame] | Err:
        if self._data is not None:
            return Ok(self._data)
        match import_df(self._file):
            case Err(e):
                msg = f"Failed to import data from {self._file}: {e}"
                return Err(FileExistsError(msg))
            case Ok(df):
                self._data = df
                return Ok(df)


@dc.dataclass(slots=True)
class SpecimenData:
    home: Path
    _data: dict[PROTOCOL_NAMES, Mapping[int, CachableData] | None]

    def __getitem__(self, name: PROTOCOL_NAMES) -> Mapping[int, CachableData] | None:
        return self._data.get(name)
