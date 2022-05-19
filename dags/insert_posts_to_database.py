from airflow.hooks.postgres_hook import PostgresHook


def insert_posts_to_database(**kwargs):
    """
    Inserts the posts into the database, by using the PostgresHook. This function is called by the DAG.
    Also, it pulls the posts from the XCOM variable and loop through them.
    """
    hook = PostgresHook(postgres_conn_id='postgres_db')
    pg_conn = hook.get_conn()
    cursor = pg_conn.cursor()

    ti = kwargs['ti']
    posts = ti.xcom_pull(task_ids='get_posts')

    for post in posts:
        cursor.execute("INSERT INTO api_json.posts (userId, id, title, body) VALUES (%s, %s, %s, %s)", (post['userId'], post['id'], post['title'], post['body']))
        pg_conn.commit()
