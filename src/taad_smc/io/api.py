# Copyright (c) 2025 Will Zhang
# pyright: reportUnknownMemberType=false
from pathlib import Path

import pandas as pd


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
