from collections.abc import Mapping
from typing import TYPE_CHECKING, get_args

from .types import PROTOCOL_NAMES, SpecimenData

if TYPE_CHECKING:
    from pytools.logging.trait import ILogger


def log_search_results(data: SpecimenData, *, log: ILogger) -> None:
    log.info(f"{'  '}Search Results:")
    for protocol in get_args(PROTOCOL_NAMES):
        log.disp(f"{'  ' * 2}Protocol: {protocol}")
        match data[protocol]:
            case Mapping() as datafiles:
                log.disp(f"{'  ' * 2}Found {len(datafiles)} files for protocol '{protocol}'.")
                for k, spec in datafiles.items():
                    log.disp(f"{'  ' * 3}Iteration {k}: {spec.file}")
            case None:
                log.disp(f"{'  ' * 2}NONE")
