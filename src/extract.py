from pathlib import Path
import pandas as pd


def load_results_data(raw_data_path: Path) -> pd.DataFrame:
    """
    Load the raw international football results dataset.

    Parameters
    ----------
    raw_data_path : Path
        Path to the raw data folder.

    Returns
    -------
    pd.DataFrame
        Raw results dataframe.
    """
    file_path = raw_data_path / "results.csv"

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_csv(file_path)

    return df