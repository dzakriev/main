from pydantic import ValidationError, Json
import db_utils
from models import get_models
from pymongo import MongoClient
from airflow import DAG
from airflow.operators.python import PythonOperator
import json


def extract(**kwargs):
    models = get_models()
    data_dict = {}
    for model in models:
        data = db_utils.fetch_all_rows(model)
        data = [row.model_dump_json() for row in data]
        print(data)
        data_dict[model.__name__] = data
    kwargs['ti'].xcom_push(key='data', value=json.dumps(data_dict))

def transform(**kwargs):
    data = kwargs["ti"].xcom_pull(task_ids='extract', key='data')

    #  no transformation needed

    kwargs['ti'].xcom_push(key='data', value=data)

def load(**kwargs):
    ti = kwargs['ti']
    data_json = ti.xcom_pull(task_ids='transform', key='data')
    data = json.loads(data_json)
    print("Starting loading data:", data)
   
    client = MongoClient("mongodb://airflow:airflow@mongodb_source:27017/")

    db = client["orders_db"]
    for table, records in data.items():
        collection = db[table]
        print("Starting loading table:", table)
        for record in records:
            try:
                collection.insert_one(json.loads(record))
            except ValidationError as e:
                print(f"Validation error for record {record}: {e}")


with DAG(
    dag_id="data_replication_dag",
) as dag:
    extract_task = PythonOperator(task_id="extract", python_callable=extract, dag=dag)
    transform_task = PythonOperator(task_id="transform", python_callable=transform, dag=dag)
    load_task = PythonOperator(task_id="load", python_callable=load, dag=dag)

    extract_task >> transform_task >> load_task
