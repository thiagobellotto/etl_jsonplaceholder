# ETL - JSONPlaceHolder
Project built for an ETL pipeline with Airflow, Docker and PostgreSQL.

It was developed with a custom version of Airflow (via Docker-Compose), by accesing the API <input type="text"><a href="https://jsonplaceholder.typicode.com/">JSONPlaceHolder</a></input> (via /posts and /users), and transforming and loading the informations into a PostgreSQL inside the Docker Container.

## Entrypoint
After cloning the repository, go to the folder and run the code below (be sure to have the docker up and running!): 

`
docker-compose -f docker-compose.yaml up airflow-init && docker-compose up
`


## First configs
The entrypoint for the PostgreSQL is the .init file, which is going to create:

`schema: json_api`

`table: users`

`table: posts`


## PGAdmin
It is useful as a GUI for the user, to query the data. The standard profile created is:

`username: airflow@airflow.com`

`password: airflow`

It is available via: <input type="text"><a href="http://localhost:5050/">localhost:5050</a></input>.


## Airflow custom configs
I have adjusted some general configs, by letting the DAGs created along with the application to run immediately and do not display the example DAGs.

But also, by letting the entrypoint and adjusting the port from the host to the container.

    AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION: 'false'
    AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
    volumes: - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports: - 15432:5432

The GUI is available via <input type="text"><a href="http://localhost:8080/">localhost:8080</a></input>.


