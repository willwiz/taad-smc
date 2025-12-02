from typing import TYPE_CHECKING

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
