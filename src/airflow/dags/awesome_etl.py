import json
import requests
import os

from datetime import timedelta, datetime

from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago

AWS_BUCKET_NAME = Variable.get('awesome_etl_bucket')
AWS_BUCKET_PREFIX = 'xl-data/awesome_etl_v1'
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

def extract_from_api(**kwargs):
    url = f'https://api.hubapi.com/crm/v3/objects/contacts?hapikey={HUBSPOT_API_KEY}'
    response = requests.get(url)
    json = response.json()
    
    # Store results in XCOM to share, in a real world solution, a reference to the data should be saved here
    task_instance = kwargs['ti']
    task_instance.xcom_push(key='contacts', value=json['results'])

def extract_from_db(**kwargs):
    hook = PostgresHook(postgres_conn_id=APP_DB_CONNECTION_ID)
    cursor = hook.get_conn().cursor()
    cursor.execute("SELECT * FROM public.contacts")
    
    # Store results in XCOM to share, in a real world solution, a reference to the data should be saved here
    task_instance = kwargs['ti']
    task_instance.xcom_push(key='contacts', value=[row for row in cursor.fetchall()])

def transform(**kwargs):
    task_instance = kwargs['ti']
    api_data = task_instance.xcom_pull(key='contacts', task_ids='extract_from_api')
    db_data = task_instance.xcom_pull(key='contacts', task_ids='extract_from_db')
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
    
    task_instance.xcom_push(key='output_file', value='/awesome_etl/output/transformed_data.json')

def load(**kwargs):
    hook = S3Hook(AWS_S3_CONNECTION_ID)
    base_key = f'{AWS_BUCKET_PREFIX}/{datetime.utcnow().isoformat()}/'
    
    task_instance = kwargs['ti']
    output_file = task_instance.xcom_pull(key='output_file', task_ids='transform')
    file_name = os.path.basename(output_file)
    hook.load_file(output_file, base_key + file_name, AWS_BUCKET_NAME)

with DAG(
    'awesome_etl_v1',
    default_args=DEFAULT_ARGS,
    schedule_interval=timedelta(days=1),
) as dag:

    exct1 = PythonOperator(
        task_id='extract_from_api',
        python_callable=extract_from_api,
        provide_context=True,
    )

    exct2 = PythonOperator(
        task_id='extract_from_db',
        python_callable=extract_from_db,
    )

    trn = PythonOperator(
        task_id='transform',
        python_callable=transform,
    )

    load = PythonOperator(
        task_id='load',
        python_callable=load,
    )

    [exct1, exct2] >> trn >> load
