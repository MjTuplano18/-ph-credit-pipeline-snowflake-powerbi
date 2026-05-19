<!--
FILE: phase_3_load.md
PURPOSE: Explain the Phase 3 loading steps into Snowflake
PHASE: 3
DEPENDS ON: RAW schema setup and load scripts
OUTPUTS: Human-readable loading notes for the project
-->

# Phase 3 - Load Into Snowflake

See phase_all_walkthrough.md for the full end-to-end guide.

## Goal

Load raw data into the RAW schema and verify tables in Snowflake.

## What We Did

- Created a Snowflake loader that reads the Lending Club CSV in chunks and loads it into RAW.
- Loaded macro data into RAW using the same loader.
- Normalized column names to uppercase for Snowflake standards.
- Used `overwrite=True` only on the first chunk for idempotency.

## Why These Steps Matter

- Chunked loading avoids memory crashes on large CSVs.
- Raw schema keeps an immutable copy of source data for auditing.
- Uppercasing column names avoids quoting issues in Snowflake SQL.

## Code Walkthrough (What Each Part Does)

### Chunked Loading

```
reader = pd.read_csv(csv_path, chunksize=chunksize)
```

This reads the large CSV in pieces so the machine does not run out of memory.

### First Chunk Overwrite

```
overwrite = index == 0
```

We overwrite only the first chunk so re-runs are safe but do not destroy later chunks.

### Snowflake Upload

```
write_pandas(..., auto_create_table=True, overwrite=overwrite)
```

`write_pandas` creates the table if missing and uploads data without manual DDL.
