# FILE: Dockerfile
# PURPOSE: Build a custom Airflow image with pipeline dependencies preinstalled
# PHASE: 6
# DEPENDS ON: requirements.txt
# OUTPUTS: Airflow image used by docker-compose

FROM apache/airflow:2.8.4-python3.10

USER root
COPY requirements.txt /requirements.txt
USER airflow
RUN pip install --no-cache-dir -r /requirements.txt
