<!--
FILE: extract_load_lending_club.md
PURPOSE: Explain the Lending Club extractor script behavior and usage
PHASE: 2
DEPENDS ON: extract/load_lending_club.py and data/lending_club.csv
OUTPUTS: Guidance for running the extractor and validating output
-->

# Lending Club Extractor

## What It Does

- Reads the Lending Club CSV in chunks to avoid memory issues.
- Adds an `ingested_at` timestamp to support data lineage.
- Prints a preview of rows and column dtypes for validation.

## How To Run

```
& .\.venv\Scripts\python.exe .\extract\load_lending_club.py
```

## Notes

- The file must be placed in `data/` and named `lending_club.csv` unless you set `LENDING_CLUB_CSV` in your environment.
- Chunked reading is mandatory to prevent crashes on large files.

## Code Walkthrough (What Each Part Does)

### Chunked CSV Reader

```
reader = pd.read_csv(csv_path, chunksize=chunksize)
```

This reads the file in chunks instead of loading everything into memory at once. It protects your machine from crashing on large files.

### Ingest Timestamp

```
chunk["ingested_at"] = pd.Timestamp.utcnow()
```

Adds a timestamp so we can audit when the data was ingested. This matters for compliance and debugging.

### Early Stop for Preview

```
if index + 1 >= max_chunks:
	break
```

Stops after a small number of chunks so Phase 2 runs quickly. Full loads happen in Phase 3.

### Safe File Check

```
if not csv_path.exists():
	raise FileNotFoundError(...)
```

Fails fast with a clear message if the CSV is missing, which saves time during debugging.
