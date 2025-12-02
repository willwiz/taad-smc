import re
from typing import TYPE_CHECKING, Literal, Required, TypedDict

from taad_smc.tdms.struct import TDMSData, TDMSMetaData

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from pwlsplit.trait import SegmentDict

__all__ = ["SpecimenInfo", "TDMSData", "TDMSMetaData", "TestProtocol"]


TEST_NAMES = Literal["Sawtooth", "Trapazoid", "Hold", "Slack", "Override"]

PROTOCOL_NAMES = Literal[
    "activation",
    "activated",
    "deactivation",
    "deactivated",
    "initial",
    "preconditioning_start",
    "preconditioning_activated",
    "preconditioning_deactivated",
    "rest_start",
    "rest_end",
]

PROTOCOLS: Mapping[PROTOCOL_NAMES, re.Pattern[str]] = {
    "activation": re.compile(r"activation_(?P<it>\d+)", re.IGNORECASE),
    "activated": re.compile(r"activated_(?P<it>\d+)", re.IGNORECASE),
    "deactivation": re.compile(r"deactivation_(?P<it>\d+)", re.IGNORECASE),
    "deactivated": re.compile(r"deactivated_(?P<it>\d+)", re.IGNORECASE),
    "initial": re.compile(r"initial_(?P<it>\d+)", re.IGNORECASE),
    "preconditioning_start": re.compile(r"preconditioning_start", re.IGNORECASE),
    "preconditioning_activated": re.compile(r"preconditioning_activated", re.IGNORECASE),
    "preconditioning_deactivated": re.compile(r"preconditioning_deactivated", re.IGNORECASE),
    "rest_start": re.compile(r"rest_start", re.IGNORECASE),
    "rest_end": re.compile(r"rest_end", re.IGNORECASE),
}


class SpecimenInfo(TypedDict):
    date: str
    species: Literal["Pig", "Human", "Sheep"]
    axis: Literal["Circ", "Long"]
    strain: float
    input_length_mm: float | int
    actual_length_mm: float | int
    details: str


class TestProtocol(TypedDict, total=False):
    """TypedDict for test protocol."""

    type: Required[TEST_NAMES]
    repeat: int
    duration: float
    max_strain: float
    loading: float
    unloading: float
    segments: Sequence[SegmentDict]
