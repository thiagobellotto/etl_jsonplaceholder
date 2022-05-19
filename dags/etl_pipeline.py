## Airflow libraries
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.http.sensors.http import HttpSensor

## Python native
from datetime import datetime
import json

## Custom libraries
from insert_posts_to_database import insert_posts_to_database
from insert_users_to_database import insert_users_to_database
from create_connections import create_connection
from transform_users import transform_users

## Create the necessary connnections to the Postgres database
create_connection(conn_id='postgres_db',
                conn_type='postgres', 
                host='host.docker.internal', 
                login='airflow', 
                schema='airflow', 
                password='airflow', 
                port='15432', 
                description='Postgres connection for Airflow')

## Create the necessary connnections to the JSON API
create_connection(conn_id='json_api',
                conn_type='http', 
                host='https://jsonplaceholder.typicode.com/', 
                login=None, 
                schema=None, 
                password=None, 
                port=None, 
                description='JSON API connection for Airflow')


with DAG('ETL_Pipeline', description='Extract, Transform and Load data from the JSONPlaceHolder API', schedule_interval='@daily', start_date=datetime(2022, 5, 18), catchup=False) as dag:

    ## Check if the API is up
    check_api = HttpSensor(
        task_id='check_api',
        http_conn_id='json_api',
        endpoint='/',
        response_check=lambda response: response.status_code == 200,
    )

    ## Extract
    ## Step 1: get the users data from the API, via endpoint /users and store into a XCOM variable
    get_users_from_api = SimpleHttpOperator(
        task_id='get_users',
        http_conn_id='json_api',
        endpoint='users/',
        method='GET',
        response_filter=lambda response: json.loads(response.text)
    )

    ## Step 2: get the posts data from the API, via endpoint /posts and store into a XCOM variable
    get_posts_from_api = SimpleHttpOperator(
        task_id='get_posts',
        http_conn_id='json_api',
        endpoint='posts/',
        method='GET',
        response_filter=lambda response: json.loads(response.text),
        log_response=True
    )

    ## Transform
    ## Step 3: Retrieve the users from XCOM, to transform and convert to a formatted JSON (new XCOM)
    transform_users = PythonOperator(
        task_id='transform_users',
        python_callable=transform_users,
        provide_context=True,
        do_xcom_push=True
    )

    ## Load
    ## Step 4: Insert the users data into the table
    insert_users_to_database = PythonOperator(
        task_id='insert_users_to_database',
        python_callable=insert_users_to_database,
        provide_context=True
    )

    ## Step 5: Insert the posts data into the table
    insert_posts_to_database = PythonOperator(
        task_id='insert_posts_to_database',
        python_callable=insert_posts_to_database,
        provide_context=True
    )

    ## Create the flows between the steps
    check_api >> get_users_from_api >> transform_users >> insert_users_to_database
    check_api >> get_posts_from_api >> insert_posts_to_database
