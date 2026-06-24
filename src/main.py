from pathlib import Path

from extract import load_results_data
from transform import (
    build_world_cup_matches_dataset,
    build_fact_matches,
    build_team_performance,
    build_world_cup_summary_by_year,
)
from load import save_dataframe


def main():
    project_root = Path(__file__).resolve().parents[1]

    raw_data_path = project_root / "data" / "raw"
    processed_data_path = project_root / "data" / "processed"
    gold_data_path = project_root / "data" / "gold"

    print("Loading raw data...")
    df_results = load_results_data(raw_data_path)

    print("Transforming World Cup data...")
    df_world_cup = build_world_cup_matches_dataset(df_results)

    print("Saving processed dataset...")
    processed_file = save_dataframe(
        df=df_world_cup,
        output_path=processed_data_path,
        file_name="world_cup_matches_processed.csv",
    )

    print("Building gold tables...")
    fact_matches = build_fact_matches(df_world_cup)
    team_performance = build_team_performance(df_world_cup)
    summary_by_year = build_world_cup_summary_by_year(df_world_cup)

    print("Saving gold tables...")
    fact_matches_file = save_dataframe(
        df=fact_matches,
        output_path=gold_data_path,
        file_name="fact_matches.csv",
    )

    team_performance_file = save_dataframe(
        df=team_performance,
        output_path=gold_data_path,
        file_name="team_performance.csv",
    )

    summary_by_year_file = save_dataframe(
        df=summary_by_year,
        output_path=gold_data_path,
        file_name="world_cup_summary_by_year.csv",
    )

    print("Pipeline completed successfully.")
    print(f"Processed rows: {len(df_world_cup):,}")
    print(f"Processed file: {processed_file}")
    print(f"Fact matches file: {fact_matches_file}")
    print(f"Team performance file: {team_performance_file}")
    print(f"Summary by year file: {summary_by_year_file}")


if __name__ == "__main__":
    main()