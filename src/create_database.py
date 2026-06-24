from pathlib import Path
import duckdb


def create_database():
    """
    Create a local DuckDB analytical database using gold layer CSV files.
    """

    project_root = Path(__file__).resolve().parents[1]

    gold_data_path = project_root / "data" / "gold"
    database_path = project_root / "database" / "world_cup.duckdb"

    database_path.parent.mkdir(parents=True, exist_ok=True)

    fact_matches_path = gold_data_path / "fact_matches.csv"
    team_performance_path = gold_data_path / "team_performance.csv"
    summary_by_year_path = gold_data_path / "world_cup_summary_by_year.csv"
    dim_date_path = gold_data_path / "dim_date.csv"
    dim_team_path = gold_data_path / "dim_team.csv"

    required_files = [
        fact_matches_path,
        team_performance_path,
        summary_by_year_path,
        dim_date_path,
        dim_team_path,
    ]

    for file_path in required_files:
        if not file_path.exists():
            raise FileNotFoundError(
                f"Required file not found: {file_path}. "
                "Run `python src/main.py` before creating the database."
            )

    print("Creating DuckDB analytical database...")

    with duckdb.connect(database_path) as con:
        con.execute("DROP TABLE IF EXISTS fact_matches")
        con.execute("DROP TABLE IF EXISTS team_performance")
        con.execute("DROP TABLE IF EXISTS world_cup_summary_by_year")
        con.execute("DROP TABLE IF EXISTS dim_date")
        con.execute("DROP TABLE IF EXISTS dim_team")

        con.execute(
            f"""
            CREATE TABLE fact_matches AS
            SELECT *
            FROM read_csv_auto('{fact_matches_path.as_posix()}')
            """
        )

        con.execute(
            f"""
            CREATE TABLE team_performance AS
            SELECT *
            FROM read_csv_auto('{team_performance_path.as_posix()}')
            """
        )

        con.execute(
            f"""
            CREATE TABLE world_cup_summary_by_year AS
            SELECT *
            FROM read_csv_auto('{summary_by_year_path.as_posix()}')
            """
        )
        
        con.execute(
            f"""
            CREATE TABLE dim_date AS
            SELECT *
            FROM read_csv_auto('{dim_date_path.as_posix()}')
            """
        )

        con.execute(
            f"""
            CREATE TABLE dim_team AS
            SELECT *
            FROM read_csv_auto('{dim_team_path.as_posix()}')
            """
        )

        tables = con.execute("SHOW TABLES").fetchdf()

        fact_count = con.execute("SELECT COUNT(*) AS rows FROM fact_matches").fetchone()[0]
        team_count = con.execute("SELECT COUNT(*) AS rows FROM team_performance").fetchone()[0]
        summary_count = con.execute(
            "SELECT COUNT(*) AS rows FROM world_cup_summary_by_year"
        ).fetchone()[0]
        dim_date_count = con.execute("SELECT COUNT(*) AS rows FROM dim_date").fetchone()[0]
        dim_team_count = con.execute("SELECT COUNT(*) AS rows FROM dim_team").fetchone()[0]

    print("Database created successfully.")
    print(f"Database path: {database_path}")
    print("\nTables created:")
    print(tables)
    print("\nRows loaded:")
    print(f"fact_matches: {fact_count:,}")
    print(f"team_performance: {team_count:,}")
    print(f"world_cup_summary_by_year: {summary_count:,}")
    print(f"dim_date: {dim_date_count:,}")
    print(f"dim_team: {dim_team_count:,}")


if __name__ == "__main__":
    create_database()