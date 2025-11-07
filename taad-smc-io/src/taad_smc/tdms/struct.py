__all__ = ["ParsedArgs", "TDMSData", "TDMSMetaData"]
import dataclasses as dc
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from pytools.arrays import A1


@dc.dataclass(slots=True, frozen=True)
class TDMSMetaData:
    name: str
    file_ver: int
    channel: int
    fiber: float
    force: float
    command: float
    position: float
    experiment_num: int | None
    operator: str | None
    operator_num: int | None
    comments: str
    daq_rate: int
    analog_freq: int
    terminal_config: int
    force_voltage_range: float
    position_voltage_range: float


@dc.dataclass(slots=True)
class TDMSData[F: np.floating]:
    time: A1[F]
    disp: A1[F]
    force: A1[F]
    command: float
    fiber_length: float
    initial_force: float
    initial_position: float
    meta: TDMSMetaData


@dc.dataclass(slots=True)
class ParsedArgs:
    input_file: str
    output_file: str | None
