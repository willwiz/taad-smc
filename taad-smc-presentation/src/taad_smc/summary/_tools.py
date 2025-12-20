from typing import TYPE_CHECKING

import numpy as np
from pytools.result import Err, Ok

if TYPE_CHECKING:
    import pandas as pd
    from taad_smc.io.api import SpecimenData
    from taad_smc.io.types import PROTOCOL_NAMES


def get_last_valid(database: SpecimenData, key: PROTOCOL_NAMES) -> Ok[pd.DataFrame | None] | Err:
    match database[key]:
        case None:
            return Ok(None)
        case datafiles:
            data = datafiles[max(datafiles.keys())]
    match data.v():
        case Ok(df):
            return Ok(df)
        case Err(e):
            return Err(e)


def _search_for_ylim_i(
    database: SpecimenData, key: PROTOCOL_NAMES
) -> Ok[tuple[float, float] | None] | Err:
    match get_last_valid(database, key):
        case Err(e):
            return Err(e)
        case Ok(data):
            pass
    if data is None:
        return Ok(None)
    proper = ~(
        data["protocol"].str.contains("start", case=False)
        | data["protocol"].str.contains("end", case=False)
    )
    data = data[proper]
    min_force = data["force"].min()
    max_force = data["force"].max()
    padding = (max_force - min_force) * 0.03
    return Ok((min_force - padding, max_force + padding))


def search_for_ylim(database: SpecimenData) -> Ok[tuple[float, float]] | Err:
    low, high = np.inf, -np.inf
    for key in database:
        if ("precondition" in key) or ("rest" in key):
            continue
        match _search_for_ylim_i(database, key):
            case Ok((min_f, max_f)):
                low = min(low, min_f)
                high = max(high, max_f)
            case Err(e):
                return Err(e)
            case _:
                continue
    if low == np.inf or high == -np.inf:
        return Err(ValueError("No valid force data found to determine y-limits."))
    return Ok((low - 3, high + 3))
