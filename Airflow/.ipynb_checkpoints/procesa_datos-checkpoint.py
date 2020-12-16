from datetime import timedelta
import pandas as pd

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

# Argumentos por defecto
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email': ['alvaro.ortigosa@uam.es'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# DAG que se ejecuta todos los días a las 3AM (cron 0 3 * * *)
dag = DAG(
    'Gestion_Datos',
    default_args=default_args,
    description='DAG para gestion de datos',
    schedule_interval="0 3 * * *",
)

# Todas las transformaciones del notebook, explicaciones de cada paso en el mismo.
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
