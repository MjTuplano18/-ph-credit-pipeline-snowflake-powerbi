# FILE: ph_credit_etl_dag.py
# PURPOSE: Orchestrate the ELT pipeline with Airflow
# PHASE: 5
# DEPENDS ON: load/snowflake_loader.py, dbt project, Snowflake credentials
# OUTPUTS: Scheduled pipeline runs in Airflow
import os
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from pendulum import datetime

PYTHON_BIN = os.getenv("PYTHON_BIN", "python")  # Allow override in Docker or CI
DBT_BIN = os.getenv("DBT_BIN", "dbt")  # Allow override if dbt is not on PATH
AIRFLOW_HOME = os.getenv("AIRFLOW_HOME", "/opt/airflow")

DEFAULT_ARGS = {
    "owner": "spmadrid-analytics",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="ph_credit_etl",
    default_args=DEFAULT_ARGS,
    start_date=datetime(2024, 1, 1),
    schedule_interval="0 6 1 * *",  # 6 AM on the 1st of every month
    catchup=False,
    tags=["credit", "etl", "ph"],
) as dag:
    load_loans = BashOperator(
        task_id="load_loans",
        bash_command=(
            f"{PYTHON_BIN} {AIRFLOW_HOME}/load/snowflake_loader.py --mode loans"
        ),
    )

    load_bsp = BashOperator(
        task_id="load_bsp",
        bash_command=(
            f"{PYTHON_BIN} {AIRFLOW_HOME}/load/snowflake_loader.py --mode bsp"
        ),
    )

    run_dbt = BashOperator(
        task_id="run_dbt",
        bash_command=(
            f"{DBT_BIN} run --project-dir {AIRFLOW_HOME}/dbt "
            f"--profiles-dir /home/airflow/.dbt --no-partial-parse"
        ),
    )

    test_dbt = BashOperator(
        task_id="test_dbt",
        bash_command=(
            f"{DBT_BIN} test --project-dir {AIRFLOW_HOME}/dbt "
            f"--profiles-dir /home/airflow/.dbt --no-partial-parse"
        ),
    )

    [load_loans, load_bsp] >> run_dbt >> test_dbt
