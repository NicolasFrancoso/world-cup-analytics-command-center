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

def build_fact_matches(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build the main fact table for World Cup matches.

    Parameters
    ----------
    df : pd.DataFrame
        Processed World Cup matches dataframe.

    Returns
    -------
    pd.DataFrame
        Fact table with match-level information.
    """
    fact_matches = df.copy()

    fact_matches = fact_matches[
        [
            "date",
            "year",
            "month",
            "decade",
            "home_team",
            "away_team",
            "home_score",
            "away_score",
            "tournament",
            "city",
            "country",
            "neutral",
            "total_goals",
            "result",
            "home_points",
            "away_points",
            "goal_difference",
        ]
    ]

    return fact_matches


def build_team_performance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build team-level performance table from World Cup matches.

    Parameters
    ----------
    df : pd.DataFrame
        Processed World Cup matches dataframe.

    Returns
    -------
    pd.DataFrame
        Team-level performance table.
    """
    home = df[
        [
            "year",
            "home_team",
            "home_score",
            "away_score",
            "home_points",
        ]
    ].copy()

    home.columns = [
        "year",
        "team",
        "goals_for",
        "goals_against",
        "points",
    ]

    home["matches_played"] = 1
    home["wins"] = (home["points"] == 3).astype(int)
    home["draws"] = (home["points"] == 1).astype(int)
    home["losses"] = (home["points"] == 0).astype(int)

    away = df[
        [
            "year",
            "away_team",
            "away_score",
            "home_score",
            "away_points",
        ]
    ].copy()

    away.columns = [
        "year",
        "team",
        "goals_for",
        "goals_against",
        "points",
    ]

    away["matches_played"] = 1
    away["wins"] = (away["points"] == 3).astype(int)
    away["draws"] = (away["points"] == 1).astype(int)
    away["losses"] = (away["points"] == 0).astype(int)

    team_matches = pd.concat([home, away], ignore_index=True)

    team_performance = (
        team_matches.groupby(["year", "team"], as_index=False)
        .agg(
            matches_played=("matches_played", "sum"),
            wins=("wins", "sum"),
            draws=("draws", "sum"),
            losses=("losses", "sum"),
            goals_for=("goals_for", "sum"),
            goals_against=("goals_against", "sum"),
            points=("points", "sum"),
        )
    )

    team_performance["goal_difference"] = (
        team_performance["goals_for"] - team_performance["goals_against"]
    )

    team_performance["win_rate"] = (
        team_performance["wins"] / team_performance["matches_played"]
    )

    team_performance["goals_per_match"] = (
        team_performance["goals_for"] / team_performance["matches_played"]
    )

    team_performance["goals_against_per_match"] = (
        team_performance["goals_against"] / team_performance["matches_played"]
    )

    team_performance = team_performance.sort_values(
        by=["year", "points", "goal_difference", "goals_for"],
        ascending=[True, False, False, False],
    )

    return team_performance


def build_world_cup_summary_by_year(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build yearly World Cup summary table.

    Parameters
    ----------
    df : pd.DataFrame
        Processed World Cup matches dataframe.

    Returns
    -------
    pd.DataFrame
        Summary table by World Cup year.
    """
    summary_by_year = (
        df.groupby("year", as_index=False)
        .agg(
            matches=("date", "count"),
            total_goals=("total_goals", "sum"),
            avg_goals_per_match=("total_goals", "mean"),
            host_countries=("country", "nunique"),
            cities=("city", "nunique"),
            teams_home=("home_team", "nunique"),
            teams_away=("away_team", "nunique"),
        )
    )

    summary_by_year["teams"] = summary_by_year[["teams_home", "teams_away"]].max(axis=1)

    summary_by_year = summary_by_year.drop(columns=["teams_home", "teams_away"])

    return summary_by_year

def build_dim_date(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build a date dimension table based on World Cup match dates.

    Parameters
    ----------
    df : pd.DataFrame
        Processed World Cup matches dataframe.

    Returns
    -------
    pd.DataFrame
        Date dimension table.
    """
    dim_date = df[["date"]].drop_duplicates().copy()

    dim_date["date"] = pd.to_datetime(dim_date["date"])
    dim_date["year"] = dim_date["date"].dt.year
    dim_date["month"] = dim_date["date"].dt.month
    dim_date["day"] = dim_date["date"].dt.day
    dim_date["day_of_week"] = dim_date["date"].dt.day_name()
    dim_date["quarter"] = dim_date["date"].dt.quarter
    dim_date["decade"] = (dim_date["year"] // 10) * 10

    dim_date = dim_date.sort_values("date").reset_index(drop=True)

    return dim_date


def build_dim_team(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build a team dimension table using all teams that played World Cup matches.

    Parameters
    ----------
    df : pd.DataFrame
        Processed World Cup matches dataframe.

    Returns
    -------
    pd.DataFrame
        Team dimension table.
    """
    home_teams = df[["home_team"]].rename(columns={"home_team": "team"})
    away_teams = df[["away_team"]].rename(columns={"away_team": "team"})

    dim_team = pd.concat([home_teams, away_teams], ignore_index=True)
    dim_team = dim_team.drop_duplicates().sort_values("team").reset_index(drop=True)

    dim_team["team_id"] = range(1, len(dim_team) + 1)

    dim_team = dim_team[["team_id", "team"]]

    return dim_team