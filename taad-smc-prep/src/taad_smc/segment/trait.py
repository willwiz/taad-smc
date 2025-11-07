import enum
from typing import TYPE_CHECKING, Literal, TypedDict

if TYPE_CHECKING:
    from collections.abc import Sequence
    from pathlib import Path


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
    unloading_rate: float


class TestProtocol(TypedDict):
    """TypedDict for test protocol."""

    repeat: int
    type: Literal["Sawtooth", "Trapazoid", "Flat", "Slack"]
    args: Protocol


class SpecimenInfo(TypedDict):
    date: str
    species: Literal["Pig", "Human", "Sheep"]
    axis: Literal["Circ", "Long"]
    input_length_mm: float | int
    actual_length_mm: float | int
    details: str


class PeakKwargs(TypedDict, total=False):
    filter_width: int
    prominence: float


class FindPeakKwargs(TypedDict, total=False):
    prominence: float
    width: float
    wlen: int
