FROM python:3.8-slim-buster

# Airflow setup                      
ARG AIRFLOW_REQUIREMENTS=async,postgres,amazon
ENV AIRFLOW_HOME=/app/airflow
RUN mkdir -p $AIRFLOW_HOME/dags

ENV AIRFLOW_VERSION=2.1.0
ENV PYTHON_VERSION=3.8
ENV CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
RUN pip install "apache-airflow[$AIRFLOW_REQUIREMENTS]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

RUN apt update && apt -y install vim nano

EXPOSE 8080

WORKDIR $AIRFLOW_HOME

COPY entrypoint.sh .
COPY airflow.cfg .

ENTRYPOINT ["sh", "entrypoint.sh"]
