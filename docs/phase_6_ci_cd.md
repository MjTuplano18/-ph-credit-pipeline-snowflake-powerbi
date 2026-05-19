<!--
FILE: phase_6_ci_cd.md
PURPOSE: Explain the Phase 6 Docker and CI/CD steps
PHASE: 6
DEPENDS ON: Docker setup and GitHub Actions
OUTPUTS: Human-readable CI/CD notes for the project
-->

# Phase 6 - Docker and CI/CD

See phase_all_walkthrough.md for the full end-to-end guide.

## Goal

Containerize the pipeline and ensure CI passes.

## Code Walkthrough (What Each Part Does)

To be added once Docker and CI files are implemented.
## What CI Does (This Repo)

The CI workflow runs on every push or PR to main and checks that:
- Python dependencies install cleanly.
- dbt can parse and compile the project.
- Unit tests (pytest) run without failures.

This catches broken changes early, before they reach production or a demo.

## Where It Lives

- .github/workflows/ci.yml

## How It Works (Step-by-Step)

1) Check out the repo.
2) Set up Python 3.10.
3) Install requirements.txt.
4) Create a temporary dbt profile (dummy env vars are fine for compile).
5) Run `dbt compile`.
6) Run `pytest`.

## Why This Matters

- It prevents "works on my machine" problems.
- It guarantees dbt models still parse when schema changes happen.
- It enforces a consistent baseline before merges.

## CI vs CD (Quick Distinction)

- CI (Continuous Integration): Validate every change automatically.
- CD (Continuous Deployment): Automatically deploy after CI passes.

This project uses CI only for now.

## How To Extend Later

- Add linting (ruff/flake8).
- Add dbt tests (`dbt test`) if CI has valid Snowflake secrets.
- Add a deploy job for Docker images or Airflow DAGs.

## Optional: Pull GHCR Image Locally

If you want to run the exact CI-built image locally, use the GHCR override:

1) Set `GHCR_IMAGE=ghcr.io/<owner>/<repo>/ph-credit-airflow:latest` in .env
2) Run:

```
docker compose -f docker-compose.yml -f docker-compose.ghcr.yml up -d
```

## Common Mistakes

- Forgetting to update CI when requirements.txt changes.
- Running `dbt test` in CI without real Snowflake credentials.
