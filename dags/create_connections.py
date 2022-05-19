import logging
from airflow import settings
from airflow.models import Connection

def create_connection(conn_id, conn_type, host, login, schema, password, port, description):
    '''
    Function to create a connection inside the Airflow UI. It will create a connection with the following parameters:
    
    conn_id: The connection ID
    conn_type: The connection type (e.g. postgres, mysql, http, etc.)
    host: The host of the connection
    login: The login of the connection
    schema: The schema of the connection
    password: The password of the connection
    port: The port of the connection
    description: The description of the connection
    '''

    conn = Connection(conn_id=conn_id,
                      conn_type=conn_type,
                      host=host,
                      login=login,
                      schema=schema,
                      password=password,
                      port=port,
                      description=description)
    session = settings.Session()

    ## Query to check for the existence of the connection
    conn_name = session.query(Connection).filter(Connection.conn_id == conn.conn_id).first()

    if str(conn_name) == str(conn.conn_id):
        logging.warning(f"Connection {conn.conn_id} already exists")
        return None

    ## If not found, create the connection
    session.add(conn)
    session.commit()
    logging.info(Connection.log_info(conn))
    logging.info(f'Connection {conn_id} is created')
    return conn