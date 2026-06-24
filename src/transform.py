import numpy as np
import pandas as pd


def clean_results_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardize the raw results dataset.

    Parameters
    ----------
    df : pd.DataFrame
        Raw results dataframe.

    Returns
    -------
    pd.DataFrame
        Cleaned results dataframe.
    """
    df = df.copy()

    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["decade"] = (df["year"] // 10) * 10

    return df


def filter_world_cup_matches(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter only FIFA World Cup matches.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned results dataframe.

    Returns
    -------
    pd.DataFrame
        FIFA World Cup matches dataframe.
    """
    df_world_cup = df[df["tournament"] == "FIFA World Cup"].copy()

    return df_world_cup


def add_match_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add analytical features to the World Cup matches dataset.

    Parameters
    ----------
    df : pd.DataFrame
        FIFA World Cup matches dataframe.

    Returns
    -------
    pd.DataFrame
        World Cup matches dataframe with analytical features.
    """
    df = df.copy()

    df["total_goals"] = df["home_score"] + df["away_score"]

    df["result"] = np.select(
        [
            df["home_score"] > df["away_score"],
            df["home_score"] < df["away_score"],
        ],
        [
            "Home Win",
            "Away Win",
        ],
        default="Draw",
    )

    df["home_points"] = np.select(
        [
            df["home_score"] > df["away_score"],
            df["home_score"] == df["away_score"],
            df["home_score"] < df["away_score"],
        ],
        [3, 1, 0],
        default=0,
    )

    df["away_points"] = np.select(
        [
            df["away_score"] > df["home_score"],
            df["away_score"] == df["home_score"],
            df["away_score"] < df["home_score"],
        ],
        [3, 1, 0],
        default=0,
    )

    df["goal_difference"] = df["home_score"] - df["away_score"]

    return df


def build_world_cup_matches_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build the processed World Cup matches analytical dataset.

    Parameters
    ----------
    df : pd.DataFrame
        Raw results dataframe.

    Returns
    -------
    pd.DataFrame
        Processed World Cup matches dataframe.
    """
    df_clean = clean_results_data(df)
    df_world_cup = filter_world_cup_matches(df_clean)
    df_world_cup = add_match_features(df_world_cup)

    return df_world_cup