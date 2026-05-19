<!--
FILE: phase_1_setup.md
PURPOSE: Explain the Phase 1 environment setup steps and decisions
PHASE: 1
DEPENDS ON: Snowflake account creation and local Python setup
OUTPUTS: Human-readable setup notes for the project
-->

# Phase 1 - Environment Setup

See phase_all_walkthrough.md for the full end-to-end guide.

## Goal

Get a working Python environment and a verified Snowflake connection.

## What We Did

- Initialized git so changes are tracked from the beginning.
- Created a Python virtual environment to isolate dependencies.
- Added .gitignore entries to prevent secrets and large files from being committed.
- Created .env and .env.example to manage Snowflake credentials safely.
- Installed required Python packages.
- Created and ran a connection test to verify Snowflake access.

## Why These Steps Matter

- Virtual environments keep project dependencies consistent.
- .env files prevent hardcoding secrets in code.
- Snowflake warehouse auto-suspend protects free trial credits.
- Early connectivity checks avoid wasted time later.

## Checklist

- .env is filled and NOT committed
- PH_CREDIT_WH warehouse exists with AUTO_SUSPEND
- PH_CREDIT_PIPELINE database has RAW, STAGING, MART
- scripts/test_connection.py prints success

## Code Walkthrough (What Each Part Does)

### Connection Test Query

```
cursor.execute("SELECT CURRENT_VERSION()")
```

This runs a simple query to prove the connection works without changing any data.

### Safe Connection Close

```
finally:
	conn.close()
```

This ensures we do not leave open sessions, which can consume resources.
