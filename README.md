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

In order to run the DAGs in this repo you need to set up a couple of accounts first:

1. An AWS account is required to store the DAGs' results in S3. In your account you need to create an S3 bucket and an IAM user with programmatic access and with the next policy attached:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "ListObjectsInBucket",
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::<bucket-name>"
            ]
        },
        {
            "Sid": "AllObjectActions",
            "Effect": "Allow",
            "Action": "s3:*Object*",
            "Resource": [
                "arn:aws:s3:::<bucket-name>/xl-data/*",
                "arn:aws:s3:::<bucket-name>/airflow-xcom/*"
            ]
        }
    ]
}
```

> Note: replace <bucket-name> in the above snippet with the name of your own bucket and keep the path as they are, they're hardcoded in the DAG's definition, oops our fault.

2. Create an free account in [HobSpot](https://www.hubspot.com/) and then get your API key, follow [this link](https://knowledge.hubspot.com/integrations/how-do-i-get-my-hubspot-api-key) to see how.

### Setting up the environment

Copy [.env.example](.env.example) to `.env` and replace placeholders with appropriated values for them. You should already have everything you need from the previous section.
Load `.env` before running docker compose.

Installing [autoenv](https://github.com/inishchith/autoenv) or similar is recommended to automatically load your `.env` file.

### Running the project

Run `docker compose up` from the root folder, be sure .env file was loaded into your terminal session before. 
It will start all the services required to have our DAGs running.
The started services are:

* PostgreSQL database.
* Airflow, accessible from host's port 8080 (http://localhost:8080).
