<!--
FILE: phase_4_transform.md
PURPOSE: Explain the Phase 4 dbt transformation steps
PHASE: 4
DEPENDS ON: dbt project configuration and RAW data
OUTPUTS: Human-readable transformation notes for the project
-->

# Phase 4 - Transform With dbt

See phase_all_walkthrough.md for the full end-to-end guide.

## Goal

Build staging, intermediate, and mart models with tests.

## What We Did

- Added dbt project configuration and model folders.
- Created staging, intermediate, and mart SQL models.
- Added dbt tests for key fields and outputs.
- Configured schema routing so marts live in MART and staging/intermediate live in STAGING.
- Resolved data quality test failures by improving loan IDs and filtering null macro rows.

## Why These Steps Matter

- dbt provides a consistent, testable transformation layer.
- Staging keeps raw data clean without business logic.
- Mart models answer the core collections prioritization question.
- Tests prevent silent data drift (critical for finance workflows).

## How To Configure profiles.yml (Local Only)

Create `~/.dbt/profiles.yml` with your Snowflake credentials (never commit this file).

```
ph_credit_pipeline:
	target: dev
	outputs:
		dev:
			type: snowflake
			account: {{ env_var('SNOWFLAKE_ACCOUNT') }}
			user: {{ env_var('SNOWFLAKE_USER') }}
			password: {{ env_var('SNOWFLAKE_PASSWORD') }}
			role: {{ env_var('SNOWFLAKE_ROLE') }}
			warehouse: {{ env_var('SNOWFLAKE_WAREHOUSE') }}
			database: {{ env_var('SNOWFLAKE_DATABASE') }}
			schema: {{ env_var('SNOWFLAKE_SCHEMA_STAGING', 'STAGING') }}
			threads: 4
```

## Commands To Run

```
dbt debug
dbt run
dbt test
```

## Code Walkthrough (What Each Part Does)

### Staging Models

They clean and type raw data so later joins are consistent.

- `stg_loans` creates `loan_quarter` from `issue_d` for time alignment.
- `stg_bsp_rates` standardizes macro dates and filters null inflation values.

### Intermediate Model

It left-joins loans with macro indicators on quarter.

- `int_loans_enriched` preserves all loans even if macro data is missing.

### Mart Models

They aggregate default risk and create a collections priority ranking.

- `mart_default_risk` computes default rate by grade and sub-grade.
- `mart_collections_priority` ranks segments using a simple priority score.

## Schema Routing (RAW -> STAGING -> MART)

dbt defaults to the schema in `profiles.yml`. We added explicit schema routing so:

- STAGING models go to the STAGING schema.
- MART models go to the MART schema.

We also added a `generate_schema_name` macro so dbt uses the exact schema names
without adding a prefix.

## Test Fixes That Were Needed

- Many rows had a missing `id` in the raw dataset. We created a stronger
	surrogate `loan_id` so not-null and unique tests pass.
- The World Bank macro series includes some null inflation values, so we
	filter those out in staging to keep metrics reliable.

## Suggested Review Queries

Use these in Snowflake to validate the models manually:

```
select count(*) from STAGING.STG_LOANS;
select count(*) from STAGING.STG_BSP_RATES;
select count(*) from STAGING.INT_LOANS_ENRICHED;

select count(*) from MART.MART_DEFAULT_RISK;
select count(*) from MART.MART_COLLECTIONS_PRIORITY;

select * from MART.MART_DEFAULT_RISK limit 10;
select * from MART.MART_COLLECTIONS_PRIORITY order by priority_score desc limit 10;
```
