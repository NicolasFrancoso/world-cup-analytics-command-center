from pathlib import Path
import pandas as pd


def save_dataframe(df: pd.DataFrame, output_path: Path, file_name: str) -> Path:
    """
    Save a dataframe as CSV.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe to save.
    output_path : Path
        Folder where the file will be saved.
    file_name : str
        Output file name.

    Returns
    -------
    Path
        Full path of the saved file.
    """
    output_path.mkdir(parents=True, exist_ok=True)

    file_path = output_path / file_name

    df.to_csv(file_path, index=False)

    return file_path