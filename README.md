# Airflow

Companion source code for the ["4 reasons why you should use Airflow’s Taskflow API"](https://github.com/m-revetria/airflow-v2-blogpost) blog post at [blog.xmartlabs.com](blog.xmartlabs.com).

The repository is split in two main branches:
* [airflow-v1](https://github.com/xmartlabs/airflow-v2-blogpost/tree/airflow-v1): contains the code of our example DAG implemented using v1-like Airflow API. It doesn't take advantage of any of the features introduced in Taskflow.
* [airflow-v2](https://github.com/xmartlabs/airflow-v2-blogpost/tree/airflow-v2): using Taskflow, we've implemented our DAG in a short and easy-to-read manner.

These two branches above can be diff'ed to see some of the changes introduced in Taskflow.

## Structure of the project

* [`docker`](./docker/): custom Docker images
* [`docker-compose`](./docker-compose/): entry points and initialization files used by the Docker container runs with `docker compose`
* [`src/airflow`](./src/airflow/): contains the source code of our DAGs
* [`docker-compose.ylm`](./docker-compose.yaml): `docker compose` file. It will starts up Airflow and any additional service required to run the examples.

## Development setup

### Setting up the environment

Copy [.env.example](.env.example) to `.env` and replace placeholders with appropriated values for them.
Load `.env` before running docker compose.

Installing [autoenv](https://github.com/inishchith/autoenv) or similar is recommended to automatically load your `.env` file.

### Running the project

Run `docker compose up` from the root folder, be sure .env file was loaded into your terminal session before. 
It will start all the services required to have our DAGs running.
The started services are:

* PostgreSQL database.
* Airflow, accessible from host's port 8080 (http://localhost:8080).
