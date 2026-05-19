<!--
FILE: phase_all_walkthrough.md
PURPOSE: End-to-end walkthrough of the pipeline across Phases 0-7
PHASE: 0-7
DEPENDS ON: Project codebase + Docker/Airflow/dbt setup
OUTPUTS: Single reference guide for onboarding and troubleshooting
-->

# End-to-End Pipeline Walkthrough (Phases 0-7)

This guide explains the entire codebase and pipeline flow from extraction to dashboards, with key decisions and the fixes applied during setup. It is meant to help you (and future reviewers) understand how each phase fits the business question: which Philippine loan segments should collections prioritize this month.

<!-- Why this exists: it replaces jumping across separate phase docs. -->

## The Big Picture

We are building an ELT pipeline for a Philippine collections use case. Lending Club loans are a proxy for PH loan data, and BSP macro indicators (inflation/rates) provide the macro context that can shift default risk.

**High-level flow:**
1. Extract Lending Club CSV and BSP macro data.
2. Load raw data into Snowflake RAW.
3. Transform in dbt (STAGING -> MART).
4. Orchestrate in Airflow on a schedule.
5. Publish marts to a dashboard.

## Architecture (3-Layer Snowflake)

- RAW: immutable copy of source data for auditability.
- STAGING: clean, typed, renamed fields for analysis.
- MART: business-ready aggregates to prioritize collections.

<!-- Non-obvious: three layers keep raw data intact while enabling trusted transformations. -->

## Phase-by-Phase Summary

### Phase 0 - Overview
- Defines the business question and pipeline scope.
- Keeps the project centered on PH collections context and BSP macro impacts.

### Phase 1 - Environment Setup
- Python venv to isolate dependencies.
- Snowflake schemas created (RAW, STAGING, MART).
- .env used for credentials (never commit).
- Connection test validates Snowflake access early.

### Phase 2 - Extract
- Lending Club CSV read in chunks to avoid memory crashes.
- BSP macro API fetch with fallback to static data.
- Both datasets add `ingested_at` for auditability.

### Phase 3 - Load
- Loader writes to Snowflake RAW with `write_pandas`.
- Uppercases columns to match Snowflake conventions.
- Idempotent: overwrite only on the first chunk.

### Phase 4 - Transform (dbt)
- STAGING cleans raw data and types columns.
- INTERMEDIATE enriches loans with macro context.
- MART aggregates default risk and collections priority.
- Tests enforce not-null, unique, and accepted values.

### Phase 5 - Orchestrate (Airflow)
- DAG runs four tasks: `load_loans`, `load_bsp`, `run_dbt`, `test_dbt`.
- Parallel loads reduce runtime and handle independent sources.
- Retry policy mitigates transient failures.

### Phase 6 - Docker + CI/CD
- Docker runs Airflow reliably even if local Python is incompatible.
- Custom image pins Python and installs dbt + Snowflake deps.
- CI (planned) will lint, test, and validate dbt compilation.

### Phase 7 - Dashboard + README
- Power BI connects to MART tables for visual reporting.
- README explains architecture decisions and project outcomes.

## Key Files and What They Do

### Extraction
- extract/load_lending_club.py: chunked CSV read.
- extract/fetch_bsp.py: BSP macro fetch with fallback.

### Loading
- load/snowflake_loader.py: loads RAW tables with `write_pandas`.

### dbt Models
- dbt/models/staging/stg_loans.sql: cleans loans.
- dbt/models/staging/stg_bsp_rates.sql: cleans macro series.
- dbt/models/intermediate/int_loans_enriched.sql: joins loans + BSP data.
- dbt/models/mart/mart_default_risk.sql: default rates by segment.
- dbt/models/mart/mart_collections_priority.sql: priority ranking.

### Orchestration
- dags/ph_credit_etl_dag.py: Airflow DAG with four tasks.

### Docker
- docker-compose.yml: runs Postgres + Airflow services.
- docker/airflow/Dockerfile: custom Airflow image with deps.

<!-- Non-obvious: the Dockerfile removes runtime pip installs for stability. -->

## Operational Flow (What Runs When)

1. `load_loans` loads Lending Club CSV chunks into RAW.
2. `load_bsp` loads macro data into RAW.
3. `run_dbt` builds STAGING, INTERMEDIATE, and MART models.
4. `test_dbt` validates data quality.

## Fixes Applied During Setup (And Why)

### 1) Airflow tasks could not find scripts
**Root cause:** Airflow runs tasks from a temp directory, so relative paths broke.
**Fix:** Use absolute paths under `/opt/airflow` for loader and dbt commands.

### 2) `load_loans` could not find the CSV
**Root cause:** CSV path was relative to the temp working dir.
**Fix:** Resolve CSV path from the project root in the loader.

### 3) Airflow logs returning 403
**Root cause:** webserver and scheduler used different `secret_key` values.
**Fix:** Set `AIRFLOW__WEBSERVER__SECRET_KEY` in .env and recreate services.

### 4) dbt profile not found in container
**Root cause:** dbt expects `~/.dbt/profiles.yml`.
**Fix:** Mount `.dbt` to `/home/airflow/.dbt` and use env_var credentials.

### 5) dbt KeyError on `generate_schema_name.sql`
**Root cause:** stale partial parse artifacts.
**Fix:** clear `dbt/target` and disable partial parsing in Airflow commands.

### 6) Large CSV load took too long for quick testing
**Root cause:** full dataset is large.
**Fix:** set `MAX_CHUNKS=2` in .env for fast test runs.

<!-- Non-obvious: MAX_CHUNKS is only for local test speed, not production. -->

## How to Run (Docker)

```
# One-time init
Docker compose up airflow-init

# Start services
Docker compose up -d

# Open Airflow
http://localhost:8080 (admin/admin)
```

## How to Run (Local dbt)

```
# From repo root
Dbt debug
Dbt run
Dbt test
```

## Interview-Ready Takeaways

- Chose Snowflake for scalable storage and separation of compute.
- Used dbt for tested, versioned transformations.
- Orchestrated with Airflow for repeatable, observable runs.
- Preserved RAW data for auditability in a regulated context.
- Designed marts to answer collections prioritization directly.

## Knowledge Check

1) Why do we load into RAW before cleaning in STAGING?
2) What problem does `MAX_CHUNKS` solve, and why should it be removed later?
3) Why is the Airflow `secret_key` important for log access?
