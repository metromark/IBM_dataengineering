#import the libraries

from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'Mark Toledo',
    'start_date': days_ago(0),
    'email': ['mptoledo13@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# defining the DAG

dag = DAG(
    'dummy_dag',
    default_args = default_args,
    description='My dummy_dag',
    schedule_interval=timedelta(minutes=1),
)

Task1 = BashOperator(
    task_id ='Task1',
    bash_command = 'sleep 1',
    dag=dag,
)

Task2 = BashOperator(
    task_id ='Task2',
    bash_command = 'sleep 2',
    dag=dag,
)

Task3 = BashOperator(
    task_id ='Task3',
    bash_command = 'sleep 3',
    dag=dag,
)

Task1 >> Task2 >> Task3