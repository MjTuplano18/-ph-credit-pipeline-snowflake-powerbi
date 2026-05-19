# FILE: load_lending_club.py
# PURPOSE: Read Lending Club CSV in chunks and preview data for validation
# PHASE: 2
# DEPENDS ON: data/ folder contains the Lending Club CSV
# OUTPUTS: Prints a sample DataFrame head and dtypes
import os
from pathlib import Path

import pandas as pd


def load_lending_club_csv(csv_path: Path, chunksize: int = 50000, max_chunks: int = 1) -> pd.DataFrame:
    """Read the Lending Club CSV in chunks and return a preview DataFrame."""
    reader = pd.read_csv(csv_path, chunksize=chunksize)  # Chunked reading prevents memory overload

    preview_chunk = None
    for index, chunk in enumerate(reader):
        if index == 0:
            preview_chunk = chunk.copy()  # Consolidate blocks to avoid fragmentation warnings
            preview_chunk["ingested_at"] = pd.Timestamp.now("UTC")  # Timestamp for data lineage and auditing

        if index + 1 >= max_chunks:
            break  # Stop early to keep Phase 2 runs fast

    if preview_chunk is None:
        raise ValueError("No data found in CSV. Check the file path and contents.")

    return preview_chunk


def main() -> None:
    data_dir = Path("data")  # Convention: large raw files live in data/
    csv_name = os.getenv("LENDING_CLUB_CSV", "lending_club.csv")  # Allow override via env var
    csv_path = data_dir / csv_name

    if not csv_path.exists():
        raise FileNotFoundError(
            f"Expected CSV at {csv_path}. Download it from Kaggle and place it in data/."
        )

    df = load_lending_club_csv(csv_path)

    print("Lending Club preview:")
    print(df.head())
    print("\nDtypes:")
    print(df.dtypes)


if __name__ == "__main__":
    main()
