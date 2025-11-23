from typing import TYPE_CHECKING

from .types import SpecimenData

if TYPE_CHECKING:
    from pathlib import Path


def parse_directory_for_data(folder: Path) -> SpecimenData:
    return SpecimenData(home=folder)
