# pyright: reportUnknownMemberType=false
from pathlib import Path

import pandas as pd


def import_data(file: Path) -> pd.DataFrame:
    """Import data from a CSV file into an AortaData object."""
    return pd.read_csv(file)
