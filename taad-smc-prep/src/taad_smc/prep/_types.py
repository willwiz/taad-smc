from typing import TYPE_CHECKING, Protocol, TypedDict

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence
    from pathlib import Path

    from pytools.logging.trait import LOG_LEVEL
    from taad_smc.io.types import PROTOCOL_NAMES, TestProtocol


import dataclasses as dc


class ProtocolGenerator(Protocol):
    def __call__(self, strain: float, /) -> Mapping[str, TestProtocol]: ...


@dc.dataclass(slots=True)
class ParsedArguments:
    folders: Sequence[str]
    overwrite: bool
    log: LOG_LEVEL


class ProgramOptions(TypedDict, total=False):
    overwrite: bool


@dc.dataclass(slots=True)
class SpecimenTree:
    home: Path
    data: Mapping[PROTOCOL_NAMES, Mapping[int, Path]]
