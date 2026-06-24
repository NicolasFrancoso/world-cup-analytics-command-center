from pathlib import Path
import duckdb


def run_kpi_queries():
    """
    Run analytical KPI queries against the DuckDB database and save outputs as CSV files.
    """

    project_root = Path(__file__).resolve().parents[1]

    database_path = project_root / "database" / "world_cup.duckdb"
    output_path = project_root / "outputs" / "kpi_results"

    output_path.mkdir(parents=True, exist_ok=True)

    if not database_path.exists():
        raise FileNotFoundError(
            f"Database not found: {database_path}. "
            "Run `python src/create_database.py` before running KPI queries."
        )

    queries = {
        "world_cup_summary_by_year": """
            SELECT
                year,
                matches,
                total_goals,
                ROUND(avg_goals_per_match, 2) AS avg_goals_per_match,
                host_countries,
                cities,
                teams
            FROM world_cup_summary_by_year
            ORDER BY year
        """,

        "highest_scoring_world_cups": """
            SELECT
                year,
                total_goals,
                matches,
                ROUND(avg_goals_per_match, 2) AS avg_goals_per_match
            FROM world_cup_summary_by_year
            ORDER BY total_goals DESC
        """,

        "avg_goals_by_decade": """
            SELECT
                decade,
                COUNT(*) AS matches,
                SUM(total_goals) AS total_goals,
                ROUND(AVG(total_goals), 2) AS avg_goals_per_match
            FROM fact_matches
            GROUP BY decade
            ORDER BY decade
        """,

        "teams_with_most_matches": """
            SELECT
                team,
                SUM(matches_played) AS total_matches_played,
                SUM(wins) AS total_wins,
                SUM(draws) AS total_draws,
                SUM(losses) AS total_losses,
                SUM(goals_for) AS total_goals_for,
                SUM(goals_against) AS total_goals_against,
                SUM(goal_difference) AS total_goal_difference
            FROM team_performance
            GROUP BY team
            ORDER BY total_matches_played DESC
        """,

        "teams_with_most_wins": """
            SELECT
                team,
                SUM(wins) AS total_wins,
                SUM(matches_played) AS total_matches_played,
                ROUND(SUM(wins) * 1.0 / SUM(matches_played), 3) AS historical_win_rate
            FROM team_performance
            GROUP BY team
            HAVING SUM(matches_played) >= 10
            ORDER BY total_wins DESC
        """,

        "best_historical_win_rate": """
            SELECT
                team,
                SUM(matches_played) AS total_matches_played,
                SUM(wins) AS total_wins,
                ROUND(SUM(wins) * 1.0 / SUM(matches_played), 3) AS historical_win_rate
            FROM team_performance
            GROUP BY team
            HAVING SUM(matches_played) >= 10
            ORDER BY historical_win_rate DESC
        """,

        "best_offensive_teams": """
            SELECT
                team,
                SUM(goals_for) AS total_goals_for,
                SUM(matches_played) AS total_matches_played,
                ROUND(SUM(goals_for) * 1.0 / SUM(matches_played), 2) AS goals_per_match
            FROM team_performance
            GROUP BY team
            HAVING SUM(matches_played) >= 10
            ORDER BY total_goals_for DESC
        """,

        "best_defensive_teams": """
            SELECT
                team,
                SUM(goals_against) AS total_goals_against,
                SUM(matches_played) AS total_matches_played,
                ROUND(SUM(goals_against) * 1.0 / SUM(matches_played), 2) AS goals_against_per_match
            FROM team_performance
            GROUP BY team
            HAVING SUM(matches_played) >= 10
            ORDER BY goals_against_per_match ASC
        """,

        "biggest_wins": """
            SELECT
                date,
                year,
                home_team,
                away_team,
                home_score,
                away_score,
                total_goals,
                ABS(goal_difference) AS absolute_goal_difference,
                city,
                country
            FROM fact_matches
            ORDER BY absolute_goal_difference DESC, total_goals DESC
        """,

        "highest_scoring_matches": """
            SELECT
                date,
                year,
                home_team,
                away_team,
                home_score,
                away_score,
                total_goals,
                city,
                country
            FROM fact_matches
            ORDER BY total_goals DESC
        """,

        "result_distribution": """
            SELECT
                result,
                COUNT(*) AS matches,
                ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
            FROM fact_matches
            GROUP BY result
            ORDER BY matches DESC
        """,

        "host_country_match_volume": """
            SELECT
                country,
                COUNT(*) AS matches_hosted,
                COUNT(DISTINCT city) AS host_cities,
                COUNT(DISTINCT year) AS world_cup_editions
            FROM fact_matches
            GROUP BY country
            ORDER BY matches_hosted DESC
        """,

        "team_consistency_across_editions": """
            SELECT
                team,
                COUNT(DISTINCT year) AS world_cup_editions,
                SUM(matches_played) AS total_matches_played,
                SUM(points) AS total_points,
                SUM(wins) AS total_wins
            FROM team_performance
            GROUP BY team
            ORDER BY world_cup_editions DESC, total_matches_played DESC
        """,

        "historical_points_ranking": """
            SELECT
                team,
                SUM(points) AS total_points,
                SUM(matches_played) AS total_matches_played,
                SUM(wins) AS total_wins,
                SUM(draws) AS total_draws,
                SUM(losses) AS total_losses,
                SUM(goal_difference) AS total_goal_difference
            FROM team_performance
            GROUP BY team
            ORDER BY total_points DESC
        """,

        "duplicated_matches_check": """
            SELECT
                date,
                home_team,
                away_team,
                COUNT(*) AS records
            FROM fact_matches
            GROUP BY
                date,
                home_team,
                away_team
            HAVING COUNT(*) > 1
            ORDER BY records DESC
        """,
    }

    print("Running KPI queries...")

    with duckdb.connect(str(database_path)) as con:
        for query_name, query in queries.items():
            print(f"Executing query: {query_name}")

            df = con.execute(query).fetchdf()

            output_file = output_path / f"{query_name}.csv"
            df.to_csv(output_file, index=False)

            print(f"Saved: {output_file}")

    print("All KPI queries executed successfully.")


if __name__ == "__main__":
    run_kpi_queries()