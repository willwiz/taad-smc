# Copyright (c) 2025 Will Zhang
# pyright: reportUnknownMemberType=false

from typing import TYPE_CHECKING

import pandas as pd

if TYPE_CHECKING:
    from pathlib import Path


def import_data(file: Path) -> pd.DataFrame:
    """Return a pandas DataFrame from a CSV file.

    Parameters
    ----------
    file : Path
        Path to the CSV file to read.

    Returns
    -------
    df : pd.DataFrame
        DataFrame containing the data from the CSV file.

    """
    return pd.read_csv(file)
