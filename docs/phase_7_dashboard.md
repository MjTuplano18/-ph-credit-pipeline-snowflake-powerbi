<!--
FILE: phase_7_dashboard.md
PURPOSE: Explain the Phase 7 dashboard and README steps
PHASE: 7
DEPENDS ON: mart models and Power BI
OUTPUTS: Human-readable dashboard notes for the project
-->

# Phase 7 - Dashboard and README

## Goal

Build a live dashboard and polish documentation.

See phase_all_walkthrough.md for the full end-to-end guide.

## What We Will Build

- A Power BI dashboard connected to Snowflake MART tables.
- Three visualizations that answer the collections prioritization question.

## Primary Data Sources

- MART.MART_DEFAULT_RISK
- MART.MART_COLLECTIONS_PRIORITY

## Suggested Charts

1) Bar chart: default rate by loan grade.
2) Scatter plot: DTI vs default rate (or DTI vs risk score).
3) Scorecards: overall default rate, high-risk segments count.

## Snowflake to Power BI Setup (Summary)

1) Power BI Desktop -> Get Data -> Snowflake.
2) Server: your Snowflake account URL (example: xy12345.ap-southeast-1.snowflakecomputing.com).
3) Warehouse: your compute warehouse name (for example, COMPUTE_WH).
4) Choose DirectQuery or Import (Import is faster for dashboards with stable data).
5) Sign in with Snowflake credentials and select database + schema (MART).
6) Load MART tables: MART_DEFAULT_RISK and MART_COLLECTIONS_PRIORITY.

## Dashboard Checklist

- Connect Power BI to Snowflake using the MART schema.
- Build the three charts above.
- Add slicers for grade and sub-grade.
- Screenshot the dashboard for README.
