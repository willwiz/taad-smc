import dataclasses as dc
import re
from typing import TYPE_CHECKING, Literal

import numpy as np

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence
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
class PlotData[F: np.floating]:
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


@dc.dataclass(slots=True)
class SpecimenData:
    home: Path
    activation: Sequence[pd.DataFrame] | None = None
    activated: Sequence[pd.DataFrame] | None = None
    deactivation: Sequence[pd.DataFrame] | None = None
    deactivated: Sequence[pd.DataFrame] | None = None
    initial: Sequence[pd.DataFrame] | None = None
    rest_start: pd.DataFrame | None = None
    rest_end: pd.DataFrame | None = None
    preconditioning_start: pd.DataFrame | None = None
    preconditioning_activated: pd.DataFrame | None = None
    preconditioning_deactivated: pd.DataFrame | None = None
