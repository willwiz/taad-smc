from pprint import pformat
from typing import TYPE_CHECKING

from pytools.result import Err, Ok

from ._types import PROTOCOL_NAMES, PROTOCOLS

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping
    from pathlib import Path
    from re import Pattern


def _match_directory(folders: Iterable[Path], pattern: Pattern[str]) -> Mapping[int, Path]:
    return {
        int(f.groupdict().get("it", 1)): folder
        for folder in folders
        if (f := pattern.match(folder.name))
    }


def _check_file_exists(test: Mapping[int, Path]) -> Ok[None] | Err:
    missing_files = [f for f in test.values() if not f.exists()]
    if missing_files:
        msg = f"Missing files: {[f.name for f in missing_files]}"
        return Err(FileNotFoundError(msg))
    return Ok(None)


def find_data_subdirectories(home: Path) -> Ok[Mapping[PROTOCOL_NAMES, Mapping[int, Path]]] | Err:
    """Search directory for subfolders matching protocol patterns.

    Parameters
    ----------
    home : Path
        Path to the home directory containing protocol subfolders.

    Returns
    -------
    Mapping[PROTOCOL_NAMES, Mapping[int, Path]]
        Mapping of protocol names to iteration-numbered file paths if there were multiple done.

    """
    folders = list(home.iterdir())
    files: Mapping[PROTOCOL_NAMES, Mapping[int, Path]] = {
        k: _match_directory(folders, v) for k, v in PROTOCOLS.items()
    }
    if not files:
        msg = f"No protocol subdirectories found in {home}"
        return Err(FileExistsError(msg))
    return Ok(files)


def check_for_files(
    folders: Mapping[PROTOCOL_NAMES, Mapping[int, Path]], pattern: str = "{NAME}.csv"
) -> Ok[Mapping[PROTOCOL_NAMES, Mapping[int, Path]]] | Err:
    files: Mapping[PROTOCOL_NAMES, Mapping[int, Path]] = {
        p: {k: f / pattern.format(NAME=f.name) for k, f in protocols.items()}
        for p, protocols in folders.items()
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
