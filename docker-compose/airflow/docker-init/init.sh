#!/bin/bash
install_dependencies() {
  cd /app/airflow/docker-init/
  pip install --pre -r requirements.txt
}

install_dependencies

# DAG's output will be stored here
mkdir -p /awesome_etl/output