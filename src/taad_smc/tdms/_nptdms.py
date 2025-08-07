# pyright: reportUnknownVariableType=false, reportUnknownVariableType=false, reportUnknownMemberType=false, reportArgumentType=none, reportUnknownArgumentType=false, reportMissingTypeStubs=false
__all__ = ["import_tdms_muscle_typeless"]
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
from nptdms import TdmsFile, TdmsGroup

from .struct import TDMSData, TDMSMetaData

if TYPE_CHECKING:
    from arraystubs import Arr1


def import_tdms_muscle_typeless(file: Path) -> TDMSData[np.float64]:
    tdms = TdmsFile.read(file)
    group: TdmsGroup = tdms["Data"]
    metadata = TDMSMetaData(
        name=tdms.properties.get("name"),
        file_ver=int(tdms.properties.get("File Version")),
        channel=int(tdms.properties.get("Data Channels")),
        fiber=float(tdms.properties.get("Fiber Length")),
        force=float(tdms.properties.get("Force")),
        command=float(tdms.properties.get("Command")),
        position=float(tdms.properties.get("Position")),
        experiment_num=tdms.properties.get("ExperimentNum", None),
        operator=tdms.properties.get("Operator Name", None),
        operator_num=tdms.properties.get("OperatorNum", None),
        comments=tdms.properties.get("Comments", ""),
        daq_rate=float(tdms.properties.get("DAQ Rate")),
        analog_freq=float(tdms.properties.get("Analog Output Rate")),
        terminal_config=int(tdms.properties.get("Terminal Config")),
        force_voltage_range=float(tdms.properties.get("Force Voltage Range")),
        position_voltage_range=float(tdms.properties.get("Position Voltage Range")),
    )
    force: Arr1[np.float64] = group["Force"][:].astype(np.float64)
    disp: Arr1[np.float64] = group["Position"][:].astype(np.float64)
    time = np.arange(0, len(force)) / metadata.daq_rate
    return TDMSData(
        time=time,
        disp=disp,
        force=force,
        command=metadata.command,
        fiber_length=metadata.fiber,
        initial_force=metadata.force,
        initial_position=metadata.position,
        meta=metadata,
    )
