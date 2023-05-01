#import the libraries

from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'Mark Test',
    'start_date': days_ago(0),
    'email': ['mark@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(days=1),
}




# defining the DAG

dag = DAG(
    'process_web_log',
    default_args = default_args,
    description='DAG that processes web logs',
    schedule_interval=timedelta(days=1),
)

ABS_PATH='/home/project/airflow/dags/capstone/'
extract_data = BashOperator(
    task_id ='extract_data',
    bash_command = "cut -d' ' -f1 " + ABS_PATH + "accesslog.txt > " + ABS_PATH + "extracted_data.txt",
    dag=dag,
)

# define 2nd task
transform_data = BashOperator(
    task_id='transform_data',
    bash_command= 'grep -o "198.46.149.143" ' + ABS_PATH + "extracted_data.txt > " + ABS_PATH + "transformed_data.txt",
    dag=dag,
)

# define 3rd task
load_data = BashOperator(
    task_id='load_data',
    bash_command= 'tar -czvf ' + ABS_PATH + "weblog.tar.gz " + ABS_PATH + "transformed_data.txt",
    dag=dag,
)


# task pipeline
extract_data >> transform_data >> load_data