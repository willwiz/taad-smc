import json
import shutil as sh
from typing import TYPE_CHECKING, Unpack

from pytools.result import Err, Ok
from taad_smc.io.api import valid_specimen_info

from ._protocol import PROTOCOL_GENERATORS

if TYPE_CHECKING:
    from pathlib import Path

    from pytools.logging.trait import ILogger

    from ._types import ProgramOptions, SpecimenTree


def _validate_keyfile(keyfile: Path) -> Ok[Path] | Err:
    if not keyfile.exists():
        msg = f"Keyfile {keyfile} does not exist."
        return Err(FileExistsError(msg))
    with keyfile.open("r") as f:
        keyfile_data = json.load(f)
    if valid_specimen_info(keyfile_data):
        return Ok(keyfile)
    return Err(ValueError(f"Invalid keyfile {keyfile}"))


def specimen_infokey_loop(
    tree: SpecimenTree, *, log: ILogger, **opts: Unpack[ProgramOptions]
) -> Ok[None] | Err:
    match _validate_keyfile(tree.home / "key.json"):
        case Ok(keyfile):
            pass
        case Err(e):
            return Err(ValueError(f"Failed to validate keyfile {tree.home / 'key.json'}: {e}"))
    for subtree in tree.data.values():
        for s in subtree.values():
            if (name := s / "key.json").exists() and not opts.get("overwrite", False):
                log.debug(f"Keyfile {name} already exists, skipping.")
                continue
            sh.copy(keyfile, name)
    return Ok(None)


def protocol_generation_loop(
    tree: SpecimenTree, *, log: ILogger, **opts: Unpack[ProgramOptions]
) -> Ok[None] | Err:
    for p, subtree in tree.data.items():
        for s in subtree.values():
            if (name := s / "protocol.json").exists() and not opts.get("overwrite", False):
                log.debug(f"Protocol file {name} already exists, skipping.")
                continue
            protocol = PROTOCOL_GENERATORS[p](0.3)
            with name.open("w") as f:
                json.dump(protocol, f, indent=4)
    return Ok(None)
