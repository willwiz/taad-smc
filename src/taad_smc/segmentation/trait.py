from collections.abc import Sequence
from pathlib import Path
from typing import Literal, Required, TypedDict


class Arguments(TypedDict):
    """TypedDict for command line arguments."""

    file: Sequence[Path]


class Protocol(TypedDict, total=False):
    max_strain: Required[float]
    loading_rate: Required[float]
    duration: float


class TestProtocol(TypedDict):
    """TypedDict for test protocol."""

    repeat: int
    type: Literal["Sawtooth", "Trapazoid"]
    args: Protocol


class PeakKwargs(TypedDict, total=False):
    filter_width: int
    prominence: float
