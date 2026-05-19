<!--
FILE: phase_5_airflow.md
PURPOSE: Explain the Phase 5 Airflow orchestration steps
PHASE: 5
DEPENDS ON: Airflow setup and DAG code
OUTPUTS: Human-readable orchestration notes for the project
-->

# Phase 5 - Orchestrate With Airflow

See phase_all_walkthrough.md for the full end-to-end guide.

## Goal

Run the pipeline as a DAG and verify task success.

## What We Did

- Created an Airflow DAG with four tasks: load loans, load BSP, run dbt, test dbt.
- Configured retries, retry delays, schedule, and catchup behavior.

## Why These Steps Matter

- Parallel loading reduces total runtime when tasks are independent.
- Retries protect against transient network or API failures.
- A fixed schedule supports predictable monthly reporting.

## Code Walkthrough (What Each Part Does)

### Parallel Load Tasks

`load_loans` and `load_bsp` run in parallel because they do not depend on each other.

### dbt Run and Test

`run_dbt` builds models, and `test_dbt` validates data quality afterward.

## How To Run (Local)

1. Initialize Airflow metadata DB.
2. Create an admin user.
3. Start scheduler and webserver.
4. Trigger the DAG manually in the UI.

## Docker Fallback (Recommended if Python is unsupported)

If your local Python version is not supported by Airflow, use Docker Compose:

1. `docker-compose up airflow-init`
2. `docker-compose up -d`
3. Open `http://localhost:8080` and log in (admin/admin)
