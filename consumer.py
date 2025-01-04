from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import psycopg2
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List

# Define the Pydantic model for the table
class Record(BaseModel):
    column1: str
    column2: int
    column3: float

# Define the Python function to extract data
def extract_data(**kwargs):
    src_conn = psycopg2.connect(
        host="source_host",
        database="source_db",
        user="source_user",
        password="source_password"
    )
    cursor = src_conn.cursor()
    cursor.execute("SELECT column1, column2, column3 FROM source_table")
    rows = cursor.fetchall()
    src_conn.close()
    # Convert rows to list of dictionaries
    data = [
        Record(column1=row[0], column2=row[1], column3=row[2]).dict()
        for row in rows
    ]
    return data

# Define the Python function to transform data
def transform_data(**kwargs):
    ti = kwargs['ti']
    extracted_data = ti.xcom_pull(task_ids='extract_data')
    # Example transformation: Add a new field
    for record in extracted_data:
        record['new_field'] = "example_value"
    return extracted_data

# Define the Python function to load data
def load_data(**kwargs):
    ti = kwargs['ti']
    transformed_data = ti.xcom_pull(task_ids='transform_data')
    dest_client = MongoClient("mongodb://destination_host:27017/")
    db = dest_client["destination_db"]
    collection = db["destination_collection"]
    collection.insert_many(transformed_data)
    dest_client.close()

# Set default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['your_email@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'data_replication_dag',
    default_args=default_args,
    description='A DAG for data replication from PostgreSQL to MongoDB',
    schedule_interval=timedelta(hours=1),
    start_date=datetime(2025, 1, 1),
    catchup=False,
)

# Define tasks
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    provide_context=True,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    provide_context=True,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    provide_context=True,
    dag=dag,
)

# Set task dependencies
extract_task >> transform_task >> load_task
