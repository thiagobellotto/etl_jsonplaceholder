from airflow.hooks.postgres_hook import PostgresHook
import json


def insert_users_to_database(**kwargs):
    """
    Inserts the users into the database, by using the PostgresHook. This function is called by the DAG.
    Also, it pulls the posts from the XCOM variable (already transformed) and loop through them.
    """
    hook = PostgresHook(postgres_conn_id='postgres_db')
    pg_conn = hook.get_conn()
    cursor = pg_conn.cursor()

    ti = kwargs['ti']
    users = ti.xcom_pull(key='users_json', task_ids='transform_users')
    
    users = json.loads(users)

    for user in users:
        cursor.execute("INSERT INTO api_json.users (id, name, username, email, phone, website, suite, city, zipcode, lat, lng, catchPhrase) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (user['id'], user['name'], user['username'], user['email'], user['phone'], user['website'], user['suite'], user['city'], user['zipcode'], user['lat'], user['lng'], user['catchPhrase']))
        pg_conn.commit()