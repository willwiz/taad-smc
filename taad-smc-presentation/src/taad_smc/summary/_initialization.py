from pathlib import Path
from pprint import pformat
from typing import TYPE_CHECKING

from pytools.result import Err, Ok

from .types import PROTOCOL_NAMES, PROTOCOLS, CachableData, SpecimenData

if TYPE_CHECKING:
    import re
    from collections.abc import Iterable, Mapping


def _match_directory(folders: Iterable[Path], pattern: re.Pattern[str]) -> Mapping[int, Path]:
    return {
        int(f.groupdict().get("it", 1)): folder / Path(folder.name).with_suffix(".csv")
        for folder in folders
        if (f := pattern.match(folder.name))
    }


def _check_file_exists(test: Mapping[int, Path]) -> Ok[None] | Err:
    missing_files = [f for f in test.values() if not f.exists()]
    if missing_files:
        msg = f"Missing files: {[f.name for f in missing_files]}"
        return Err(FileNotFoundError(msg))
    return Ok(None)


def find_datafiles(home: Path) -> Ok[Mapping[PROTOCOL_NAMES, Mapping[int, Path]]] | Err:
    folders = list(home.iterdir())
    files: Mapping[PROTOCOL_NAMES, Mapping[int, Path]] = {
        k: _match_directory(folders, v) for k, v in PROTOCOLS.items()
    }
    missing_files = {
        p: str(res.val)
        for p, protocols in files.items()
        if isinstance(res := _check_file_exists(protocols), Err)
    }
    if missing_files:
        msg = f"Some data files are missing:\n {pformat(missing_files)}"
        return Err(FileExistsError(msg))
    return Ok(files)


def import_datafiles(
    home: Path,
) -> Ok[SpecimenData] | Err:
    match find_datafiles(home):
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
