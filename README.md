<<<<<<< HEAD
# Sales Analytics Data Warehouse

An end-to-end Data Engineering project built with **Python, PostgreSQL, Apache Airflow, FastAPI, and Metabase** to transform raw e-commerce data into analytics-ready datasets.

## Architecture

```text id="5y9nnv"
Olist CSV Data → Python ETL → PostgreSQL → FastAPI / Metabase
                         ↑
                    Airflow
```

Apache Kafka is included as an extension for experimenting with real-time order events.

## Tech Stack

- **Python & Pandas:** Data extraction and transformation
- **PostgreSQL:** Data warehouse
- **Apache Airflow:** Workflow orchestration
- **FastAPI:** API for accessing analytics
- **Metabase:** Data visualization
- **Docker Compose:** Local development environment
- **Apache Kafka:** Event streaming extension

## Pipeline

1. Extract data from the Olist e-commerce CSV files.
2. Clean and transform data using Python.
3. Load the data into PostgreSQL staging tables.
4. Build analytical dimensions and the sales fact table.
5. Explore sales metrics through FastAPI and Metabase.
=======
# Cloud Sales Analytics Pipeline

An end-to-end Data Engineering project built with **Apache Airflow, Google BigQuery, dbt, and Metabase** to transform raw e-commerce data into analytics-ready datasets.

## Architecture

```text
Olist CSV Data → Airflow → BigQuery → dbt → Metabase
```

## Tech Stack

- **Python:** Data ingestion and pipeline logic
- **Apache Airflow:** Workflow orchestration
- **Google BigQuery:** Cloud data warehouse
- **dbt:** SQL transformations and data modeling
- **Metabase:** Data visualization and analytics
- **Docker Compose:** Local environment
- **GitHub Actions:** dbt project validation

## Pipeline

1. Ingest Olist e-commerce data into BigQuery.
2. Organize raw data in the `olist_raw` dataset.
3. Transform data into analytical models using dbt in `dbt_olist`.
4. Connect Metabase to BigQuery for data exploration and dashboards.
>>>>>>> d82dba79cc514126f4a02af0fecd25fce56a943e

## Getting Started

Start the services:

<<<<<<< HEAD
```bash id="7xy0sw"
=======
```bash
>>>>>>> d82dba79cc514126f4a02af0fecd25fce56a943e
docker compose up -d --build
```

Check their status:

<<<<<<< HEAD
```bash id="r2gwn8"
docker compose ps
```

Stop the services:

```bash id="tcbq5e"
docker compose down
```

**Prerequisites:** Docker Desktop, the Olist dataset, and the required environment variables.

## Project Status

The project brings together ETL, data warehousing, workflow orchestration, and analytics in a local environment. Pipeline execution and data quality are validated as part of testing.

Built as part of my journey in **Data Engineering and analytics**.
=======
```bash
docker compose ps
```

**Prerequisites:** Docker Desktop, a configured Google Cloud project, BigQuery permissions, and the required environment variables and credentials.


## Project Status

The local environment is running, with Airflow and Metabase operational. End-to-end ingestion and dbt model execution are still being validated.

Built as part of my journey in **Data Engineering and cloud data platforms**.
>>>>>>> d82dba79cc514126f4a02af0fecd25fce56a943e
