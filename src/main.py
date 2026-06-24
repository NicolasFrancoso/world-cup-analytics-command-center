from pathlib import Path

from extract import load_results_data
from transform import build_world_cup_matches_dataset
from load import save_dataframe


def main():
    project_root = Path(__file__).resolve().parents[1]

    raw_data_path = project_root / "data" / "raw"
    processed_data_path = project_root / "data" / "processed"

    print("Loading raw data...")
    df_results = load_results_data(raw_data_path)

    print("Transforming World Cup data...")
    df_world_cup = build_world_cup_matches_dataset(df_results)

    print("Saving processed dataset...")
    output_file = save_dataframe(
        df=df_world_cup,
        output_path=processed_data_path,
        file_name="world_cup_matches_processed.csv",
    )

    print(f"Pipeline completed successfully.")
    print(f"Rows processed: {len(df_world_cup):,}")
    print(f"Output file: {output_file}")


if __name__ == "__main__":
    main()