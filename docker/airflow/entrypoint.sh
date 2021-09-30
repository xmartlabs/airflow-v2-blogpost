#!/bin/bash
airflow db init
airflow users create \
    --username admin \
    --firstname Peter \
    --lastname Parker \
    --role Admin \
    --email spiderman@superhero.org \
    --password admin
airflow scheduler &>./scheduler.log &
airflow webserver -p 8080
