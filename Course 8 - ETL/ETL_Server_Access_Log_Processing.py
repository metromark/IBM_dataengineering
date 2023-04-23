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
    'ETL_Server_Access_Log_Processing',
    default_args = default_args,
    description='My ETL_Server_Access_Log_Processing',
    schedule_interval=timedelta(days=1),
)


download = BashOperator(
    task_id ='download',
    bash_command = 'wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Apache%20Airflow/Build%20a%20DAG%20using%20Airflow/web-server-access-log.txt',
    dag=dag,
)

extract = BashOperator(
    task_id ='extract',
    bash_command = 'grep -oE (timestamp|visitorid)=[^ ]* /home/project/web-server-access-log.txt > /home/project/airflow/dags/extracted_logs.txt',
    dag=dag,
)

transform = BashOperator(
    task_id ='transform',
    bash_command = 'tr "[a-z] [A-Z]" /home/project/extracted_logs.txt > /home/project/airflow/dags/transformed_logs.txt',
    dag=dag,
)

load = BashOperator(
    task_id ='load',
    bash_command = 'zip log.zip /home/project/transformed_logs.txt',
    dag=dag,
)

# task pipeline block

download >> extract >> transform >> load