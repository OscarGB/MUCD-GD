from datetime import timedelta
import pandas as pd

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to operate!
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}

dag = DAG(
    'Gestion_Datos',
    default_args=default_args,
    description='DAG para gestion de datos',
    schedule_interval="0 3 * * *",
)

# Todas las transformaciones del Jupyter, referir a él para comprender cada paso.
def processData():
    ratings = pd.read_csv("~/ratings.csv")
    ratings.timestamp = pd.to_datetime(ratings.timestamp, unit='s')
    movies = pd.read_csv("~/movies.csv")
    ratings.dropna(axis="index", subset=["rating"], inplace=True)
    ratings = ratings[(0.5 <= ratings.rating) & (ratings.rating <= 5)]
    ratings.rating = (ratings.rating*2).round()/2
    movies = movies.assign(genres=movies.genres.str.split('|')).explode('genres')
    ratings = ratings.merge(movies, on="movieId", how="left")
    ratings = ratings[["rating", "timestamp", "genres"]]
    ratings.to_csv("~/pelis_procesadas.csv")
    
# Operador python que ejecuta la función de transformación de datos.
do_everything = PythonOperator(
                    task_id='process_data',
                    python_callable=processData,
                    op_kwargs=None,
                    dag=dag)
