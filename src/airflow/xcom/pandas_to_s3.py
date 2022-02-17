from airflow.models.xcom import BaseXCom
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

import pandas as pd
import uuid

AWS_BUCKET_PREFIX = 'airflow-xcom'

class PandasToS3XComBackend(BaseXCom):
  DATA_SCHEMA = "awesome-etl-s3://"

  @staticmethod
  def serialize_value(value):
    if isinstance(value, pd.DataFrame):
      from airflow.models import Variable

      bucket = Variable.get('awesome_etl_bucket')
      hook = S3Hook(Variable.get('awesome_etl_aws_connection_id'))
      file_name = f'data_{str(uuid.uuid4())}.json'
      key = f'{AWS_BUCKET_PREFIX}/{file_name}'

      with open(file_name, 'w') as file:
        value.to_csv(file)
      hook.load_file(file_name, key, bucket, replace=True)
      
      value = PandasToS3XComBackend.DATA_SCHEMA + key
    
    return BaseXCom.serialize_value(value)

  @staticmethod
  def deserialize_value(result):
    result = BaseXCom.deserialize_value(result)
    if isinstance(result, str) and result.startswith(PandasToS3XComBackend.DATA_SCHEMA):
      from airflow.models import Variable
      bucket = Variable.get('awesome_etl_bucket')
      hook = S3Hook(Variable.get('awesome_etl_aws_connection_id'))
      key = result.replace(PandasToS3XComBackend.DATA_SCHEMA, "")
      file_name = hook.download_file(key, bucket, "/tmp")
      result = pd.read_csv(file_name)
    
    return result


  def orm_deserialize_value(self):
    result = BaseXCom.deserialize_value(self)
    if isinstance(result, str) and result.startswith(PandasToS3XComBackend.DATA_SCHEMA):
      result = f'{result} (serialized by "PandasToS3XComBackend")'
    return result
