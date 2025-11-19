from typing import Literal, Required, TypedDict

from taad_smc.tdms.struct import TDMSData, TDMSMetaData

__all__ = ["SpecimenInfo", "TDMSData", "TDMSMetaData", "TestProtocol"]


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

    type: Required[Literal["Sawtooth", "Trapazoid", "Hold", "Slack"]]
    repeat: int
    duration: float
    max_strain: float
    loading: float
    unloading: float
