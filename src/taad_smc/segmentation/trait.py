import enum
from collections.abc import Sequence
from pathlib import Path
from typing import Literal, TypedDict


class CurveSegment(enum.StrEnum):
    STRETCH = "STRETCH"
    HOLD = "HOLD"
    RECOVER = "RECOVER"


class CurvePoint(enum.Enum):
    PEAK = enum.auto()
    VALLEY = enum.auto()


class Arguments(TypedDict):
    """TypedDict for command line arguments."""

    file: Sequence[Path]


class Protocol(TypedDict, total=False):
    max_strain: float
    loading_rate: float
    duration: float


class TestProtocol(TypedDict):
    """TypedDict for test protocol."""

    repeat: int
    type: Literal["Sawtooth", "Trapazoid", "Flat", "Slack"]
    args: Protocol


class PeakKwargs(TypedDict, total=False):
    filter_width: int
    prominence: float


class FindPeakKwargs(TypedDict, total=False):
    prominence: float
    width: float
    wlen: int
