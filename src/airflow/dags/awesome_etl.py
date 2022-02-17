import json
import requests
import os

from datetime import timedelta, datetime

from airflow.decorators import dag, task, task_group
from airflow.models import Variable
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.postgres.hooks.postgres import PostgresHook

from airflow.utils.dates import days_ago

import pandas as pd

AWS_BUCKET_NAME = Variable.get('awesome_etl_bucket')
AWS_BUCKET_PREFIX = 'xl-data/awesome_etl_v2'
AWS_S3_CONNECTION_ID = Variable.get('awesome_etl_aws_connection_id')
APP_DB_CONNECTION_ID = Variable.get('awesome_etl_app_db_connection_id')

HUBSPOT_API_KEY = Variable.get('awesome_etl_hubspot_api_key')
if not HUBSPOT_API_KEY:
    raise ValueError('awesome_etl_hubspot_api_key variable must be set with a valid Hubspot API KEY.')

DEFAULT_ARGS = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['miguel@xmartlabs.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': days_ago(2),
}

@dag(default_args=DEFAULT_ARGS, schedule_interval='@Daily')
def awesome_etl_v2():

    @task_group()
    def extract():
        @task()
        def extract_from_api():
            url = f'https://api.hubapi.com/crm/v3/objects/contacts?hapikey={HUBSPOT_API_KEY}'
            response = requests.get(url)
            json = response.json()
            return {'contacts': json['results']}

        @task()
        def extract_from_db():
            hook = PostgresHook(postgres_conn_id=APP_DB_CONNECTION_ID)
            cursor = hook.get_conn().cursor()
            cursor.execute("SELECT * FROM public.contacts")
            return {
                'contacts': [row for row in cursor.fetchall()]
            }

        return {
            'api_data': extract_from_api(),
            'db_data': extract_from_db(),
        }

    @task()
    def transform(data):
        api_data = data['api_data']['contacts']
        db_data = data['db_data']['contacts']
        data = []
        for api_row in api_data:
            email = api_row.get('properties', {}).get('email', None)
            db_row = next((x for x in db_data if x[1] == email), None)
            row = {
            'db_id': db_row[0],
            'api_id': api_row['id'],
            'email': email,
            'created_at': api_row.get('createdAt'),
            'hero_name': db_row[4],
            'address': db_row[5],
            'favorite_color': db_row[6],
            'full_name': f"{api_row.get('properties', {}).get('firstname')} {api_row.get('properties', {}).get('lastname')}",
            'api_archived': api_row.get('archived')
            }
            data.append(row)

        with open('/awesome_etl/output/transformed_data.json', 'w') as file:
            for row in data:
                file.write(json.dumps(row))
                file.write('\n')
        
        return { 'output_file': '/awesome_etl/output/transformed_data.json' }

    @task()
    def load(output):
        hook = S3Hook(AWS_S3_CONNECTION_ID)
        base_key = f'{AWS_BUCKET_PREFIX}/{datetime.utcnow().isoformat()}/'
        file_name = os.path.basename(output['output_file'])
        hook.load_file(output['output_file'], base_key + file_name, AWS_BUCKET_NAME)

    load(transform(extract()))


etl_dag = awesome_etl_v2()


@dag(default_args=DEFAULT_ARGS, schedule_interval='@Daily')
def custom_xcom_dag():
    @task
    def write_xcom_backend():
        return pd.DataFrame.from_dict({
            'id': [123, 234, 345],
            'date': [1643724967, 1643723967, 1643714967],
            'name': ['spiderman', 'ironman', 'hulk']
        })
    
    @task
    def read_xcom_backend(data_frame):
        print(f'data_frame => {data_frame}')

    read_xcom_backend(write_xcom_backend())


custom_xcom_dag = custom_xcom_dag()