"""Summarize activation data."""

from typing import TYPE_CHECKING, Literal

import numpy as np
from pytools.result import Err, Ok

from ._tools import get_last_valid
from .types import PlotData, SpecimenData

if TYPE_CHECKING:
    from collections.abc import Mapping

    import pandas as pd
    from pytools.logging.trait import ILogger


def parse_activation_data(
    database: SpecimenData,
) -> Ok[Mapping[Literal["activation", "deactivation", "initial"], pd.DataFrame]] | Err:
    match get_last_valid(database, "activation"):
        case Err(e):
            return Err(e)
        case Ok(activation_data):
            pass
    match get_last_valid(database, "deactivation"):
        case Err(e):
            return Err(e)
        case Ok(deactivation_data):
            pass
    match get_last_valid(database, "initial"):
        case Err(e):
            return Err(e)
        case Ok(initial_data):
            pass
    data: Mapping[Literal["activation", "deactivation", "initial"], pd.DataFrame | None] = {
        "activation": activation_data,
        "deactivation": deactivation_data,
        "initial": initial_data,
    }
    data = {k: v[v["protocol"] == "Relax_Slow"] for k, v in data.items() if v is not None}
    return Ok(data)


def create_plot_data(
    data: Mapping[Literal["activation", "deactivation", "initial"], pd.DataFrame],
) -> Mapping[Literal["activation", "deactivation", "initial"], PlotData[np.float64]]:
    return {
        k: PlotData(x=df["time"].to_numpy(dtype=np.float64), y=df["force"].to_numpy(np.float64))
        for k, df in data.items()
    }


def summarize_activation_data(database: SpecimenData, *, log: ILogger) -> Ok[None] | Err:
    match parse_activation_data(database):
        case Ok(data):
            if not data:
                log.info("No activation-related data found. Skipping ...")
                return Ok(None)
        case Err(e):
            return Err(e)
    return Ok(None)
