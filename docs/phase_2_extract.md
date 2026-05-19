<!--
FILE: phase_2_extract.md
PURPOSE: Explain the Phase 2 data extraction steps and scripts
PHASE: 2
DEPENDS ON: extract/ scripts and data/ inputs
OUTPUTS: Human-readable extraction notes for the project
-->

# Phase 2 - Extract Data

See phase_all_walkthrough.md for the full end-to-end guide.

## Goal

Extract both data sources and validate them as DataFrames.

## Scripts

- extract/load_lending_club.py
- extract/fetch_bsp.py (to be added)

## Related Docs

- extract_load_lending_club.md
- extract_fetch_bsp.md

## Code Walkthrough (What Each Part Does)

See `extract_load_lending_club.md` for the detailed walkthrough of the current extractor.

## Notes

- Lending Club CSV must be read in chunks to avoid memory issues.
- BSP API needs a fallback to static data for reliability.
- Add ingested_at timestamps for auditability.
