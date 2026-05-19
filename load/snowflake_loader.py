# FILE: snowflake_loader.py
# PURPOSE: Load raw loan and macro data into Snowflake RAW schema
# PHASE: 3
# DEPENDS ON: .env with Snowflake credentials and BSP_API_URL
# OUTPUTS: RAW.RAW_LOANS and RAW.RAW_BSP_RATES tables in Snowflake
import argparse
import os
import sys
from pathlib import Path

import pandas as pd
import snowflake.connector
from dotenv import load_dotenv
from snowflake.connector.pandas_tools import write_pandas

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))  # Allow imports from project root when run as a script

from extract.fetch_bsp import fetch_bsp_rates


def _require_env(var_name: str) -> str:
    value = os.getenv(var_name)
    if not value:
        raise ValueError(f"Missing required environment variable: {var_name}")
    return value


def _uppercase_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [col.upper() for col in df.columns]
    return df


def load_lending_club_to_snowflake(
    conn: snowflake.connector.SnowflakeConnection,
    csv_path: Path,
    schema: str,
    chunksize: int = 50000,
    max_chunks: int | None = None,
) -> None:
    reader = pd.read_csv(
        csv_path,
        chunksize=chunksize,
        dtype=str,
    )  # Chunked reading prevents memory overload and avoids mixed-type errors

    for index, chunk in enumerate(reader):
        chunk = chunk.copy()
        chunk = chunk.astype("string")
        chunk["INGESTED_AT"] = pd.Timestamp.now("UTC")
        chunk = chunk.reset_index(drop=True)
        chunk = _uppercase_columns(chunk)

        overwrite = index == 0  # Only overwrite on the first chunk for idempotency
        success, _, _, _ = write_pandas(
            conn,
            chunk,
            table_name="RAW_LOANS",
            schema=schema,
            auto_create_table=True,
            overwrite=overwrite,
            use_logical_type=True,
        )

        if not success:
            raise RuntimeError("Failed to load a chunk into RAW.RAW_LOANS")

        if max_chunks is not None and index + 1 >= max_chunks:
            break  # Keep loads bounded for local testing


def load_bsp_to_snowflake(
    conn: snowflake.connector.SnowflakeConnection,
    schema: str,
    api_url: str,
) -> None:
    df = fetch_bsp_rates(api_url)
    df = _uppercase_columns(df)

    success, _, _, _ = write_pandas(
        conn,
        df,
        table_name="RAW_BSP_RATES",
        schema=schema,
        auto_create_table=True,
        overwrite=True,
        use_logical_type=True,
    )

    if not success:
        raise RuntimeError("Failed to load data into RAW.RAW_BSP_RATES")


def main() -> None:
    parser = argparse.ArgumentParser(description="Load raw data into Snowflake")
    parser.add_argument(
        "--mode",
        choices=["all", "loans", "bsp"],
        default="all",
        help="Select which datasets to load",
    )
    args = parser.parse_args()

    load_dotenv()  # Load local .env values

    account = _require_env("SNOWFLAKE_ACCOUNT")
    user = _require_env("SNOWFLAKE_USER")
    password = _require_env("SNOWFLAKE_PASSWORD")
    role = _require_env("SNOWFLAKE_ROLE")
    warehouse = _require_env("SNOWFLAKE_WAREHOUSE")
    database = _require_env("SNOWFLAKE_DATABASE")
    schema_raw = os.getenv("SNOWFLAKE_SCHEMA_RAW", "RAW")
    api_url = os.getenv("BSP_API_URL", "")
    max_chunks_env = os.getenv("MAX_CHUNKS")
    chunksize_env = os.getenv("CHUNKSIZE")

    max_chunks = int(max_chunks_env) if max_chunks_env else None
    chunksize = int(chunksize_env) if chunksize_env else 50000

    csv_path = ROOT_DIR / "data" / os.getenv("LENDING_CLUB_CSV", "lending_club.csv")
    if args.mode in {"all", "loans"} and not csv_path.exists():
        raise FileNotFoundError(
            f"Expected CSV at {csv_path}. Download it from Kaggle and place it in data/."
        )

    conn = snowflake.connector.connect(
        account=account,
        user=user,
        password=password,
        role=role,
        warehouse=warehouse,
        database=database,
    )

    try:
        if args.mode in {"all", "loans"}:
            load_lending_club_to_snowflake(
                conn,
                csv_path,
                schema_raw,
                chunksize=chunksize,
                max_chunks=max_chunks,
            )

        if args.mode in {"all", "bsp"}:
            load_bsp_to_snowflake(conn, schema_raw, api_url)

        print(f"SUCCESS: Loaded mode={args.mode}")
    finally:
        conn.close()  # Always close the connection to avoid leaking sessions


if __name__ == "__main__":
    main()
