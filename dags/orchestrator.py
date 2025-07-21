import sys
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta


sys.path.append('/opt/airflow/api_request') 
from insert_records import main


default_args = {
    'descriptions': "A DAG to orchestrate data",
    'start_date': datetime(2025, 7, 17), 
    'catchup': False
}

dag = DAG(
    dag_id = "weather-api-dbt-orchestrator",
    default_args=default_args,
    schedule=timedelta(minutes=5)
)

with dag:
    task1 = PythonOperator(
        task_id='ingest_data_tasks',
        python_callable=main
    )
    
    # dbt_run = BashOperator(
    #     task_id='dbt_run',
    #     bash_command='cd /opt/airflow/dbt_weatherstack && dbt run',
    # )
    
    # dbt_test = BashOperator(
    #     task_id='dbt_test',
    #     bash_command='cd /opt/airflow/dbt_weatherstack && dbt test',
    # )

task1 #>> dbt_run >> dbt_test