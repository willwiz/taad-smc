from typing import TYPE_CHECKING, get_args

from .types import PROTOCOL_NAMES

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path

    from pytools.logging.trait import ILogger


def print_datafound(files: Mapping[PROTOCOL_NAMES, Mapping[int, Path]], *, log: ILogger) -> None:
    log.info("Search Results:")
    for protocol in get_args(PROTOCOL_NAMES):
        log.disp(f"Protocol: {protocol}")
        match files.get(protocol):
            case dict(datafiles):
                log.disp(f"  Found {len(datafiles)} files for protocol '{protocol}'.")
                for it, filepath in datafiles.items():
                    log.disp(f"    Iteration {it}: {filepath}")
            case _:
                log.disp("  NONE")
