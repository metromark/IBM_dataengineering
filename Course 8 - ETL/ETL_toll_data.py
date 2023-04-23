#import the libraries

from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

ABS_PATH='/home/project/airflow/dags/finalassignment/'

default_args = {
    'owner': 'Mark Test',
    'start_date': days_ago(0),
    'email': ['test@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# defining the DAG

dag = DAG(
    'ETL_toll_data',
    default_args = default_args,
    description='Apache Airflow Final Assignment',
    schedule_interval=timedelta(days=1),
)

unzip_data = BashOperator(
    task_id ='unzip_data',
    bash_command = 'cd ' + ABS_PATH + '&& tar -xf tolldata.tgz -C ./',
    dag=dag,
)

extract_data_from_csv = BashOperator(
    task_id ='extract_data_from_csv',
    bash_command = 'cut -d"," -f1-4 ' + ABS_PATH + 'vehicle-data.csv > ' + ABS_PATH + 'csv_data.csv',
    dag=dag,
)

# preprocess_tsv = BashOperator(
#     task_id ='preprocess_tsv',
#     bash_command = 'cut -f1-7 ' + ABS_PATH + 'tollplaza-data.tsv|tr -d "\r" > ' + ABS_PATH + 'test.csv' ,
#     dag=dag,
# )


extract_data_from_tsv = BashOperator(
    task_id ='extract_data_from_tsv',
    bash_command = "cut -d$'\t' -f5,6,7 " + ABS_PATH + 'tollplaza-data.tsv | tr "\t" ","  > ' + ABS_PATH + 'tsv_data.csv',
    dag=dag,
)

extract_data_from_fixed_width = BashOperator(
    task_id ='extract_data_from_fixed_width',
    bash_command = 'cut -b 59-67 ' + ABS_PATH + "payment-data.txt  | tr ' ' ','  > " + ABS_PATH + 'fixed_width_data.csv' ,
    dag=dag,
)

consolidate_data = BashOperator(
    task_id ='consolidate_data',
    bash_command = 'paste -d "," ' + ABS_PATH + 'csv_data.csv ' + ABS_PATH + 'tsv_data.csv ' + ABS_PATH + 'fixed_width_data.csv > ' + ABS_PATH + 'extracted_data.csv',
    dag=dag,
)

transform_data = BashOperator(
    task_id ='transform_data',
    bash_command = 'tr [:lower:] [:upper:] < '+ ABS_PATH +'extracted_data.csv > '+ ABS_PATH +'transformed_data.csv',
    dag=dag,
)

unzip_data >> extract_data_from_csv >> extract_data_from_tsv >> extract_data_from_fixed_width >> consolidate_data >> transform_data