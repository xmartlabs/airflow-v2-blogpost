# Airflow

## Structure of the project

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
