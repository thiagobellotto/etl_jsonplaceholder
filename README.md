# ETL - JSONPlaceHolder
Project built for an ETL pipeline with Airflow, Docker and PostgreSQL.

It was developed with a custom version of Airflow (via Docker-Compose), by accesing the API <input type="text"><a href="https://jsonplaceholder.typicode.com/">JSONPlaceHolder</a></input> (via /posts and /users), and transforming and loading the informations into a PostgreSQL inside the Docker Container.

## Create an .env file
When running for the first time, it is necessary to create an .env file. Store this two variables inside:

`AIRFLOW_UID=50000`

`AIRFLOW_GID=0`


## Entrypoint
After cloning the repository, go to the folder and run the code below (be sure to have the docker up and running!): 

For the first time: `mkdir logs plugins`

Everytime: `docker-compose -f docker-compose.yaml up airflow-init && docker-compose up`


## First configs
The entrypoint for the PostgreSQL is the .init file, which is going to create:

`schema: json_api`

`table: users`

`table: posts`


## PGAdmin
It is useful as a GUI for the user, to query the data. It is available via: <input type="text"><a href="http://localhost:5050/">localhost:5050</a></input>. The standard profile created is:

`username: airflow@airflow.com`

`password: airflow`

To connect with the server, go to "Add New Server", name the server and set the below infos:

`Host name/Address: host.docker.internal`

`Port: 15432`

`Maintenance Database: airflow`

`Username: airflow`

`Password: airflow`


## Conections
The connections needed are created programatically, there is no need to insert them manually. There are two:

- HTTP, for connecting with the API;
- Postgres, to connect with the database.


## Airflow custom configs
I have adjusted some general configs, by letting the DAGs created along with the application to run immediately and do not display the example DAGs.

But also, by letting the entrypoint and adjusting the port from the host to the container.

    AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION: 'false'
    AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
    volumes: - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports: - 15432:5432

The GUI is available via <input type="text"><a href="http://localhost:8080/">localhost:8080</a></input>.

## Flow from the DAGs

![image](https://user-images.githubusercontent.com/17580929/169189278-4b2abf85-bdb4-4dc5-bd89-e4acf4c287b4.png)


## Query the database via PGAdmin

![image](https://user-images.githubusercontent.com/17580929/169189339-7e957cca-8cd4-4ec1-affc-1a99b17662cc.png)

