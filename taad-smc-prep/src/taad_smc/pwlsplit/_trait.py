import dataclasses as dc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from pytools.logging.trait import LogLevel


@dc.dataclass(slots=True)
class SegmentOptions:
    plot: bool
    overwrite: bool
    log: LogLevel


@dc.dataclass(slots=True)
class FileNames:
    raw: Path
    csv: Path
    protocol: Path
    info: Path
