from typing import TYPE_CHECKING

from pytools.result import Err, Ok
from taad_smc.io.api import CachableData, SpecimenData, check_for_files, find_data_subdirectories

if TYPE_CHECKING:
    from pathlib import Path


def import_datafiles(
    home: Path,
) -> Ok[SpecimenData] | Err:
    match find_data_subdirectories(home):
        case Ok(folders):
            pass
        case Err(e):
            return Err(e)
    match check_for_files(folders):
        case Ok(datafiles):
            data = SpecimenData(
                home,
                {
                    p: {k: CachableData(f) for k, f in files.items()}
                    for p, files in datafiles.items()
                },
            )
        case Err(e):
            return Err(e)
    return Ok(data)
