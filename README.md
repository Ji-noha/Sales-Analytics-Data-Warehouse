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

## Getting Started

Start the services:

```bash
docker compose up -d --build
```

Check their status:

```bash
docker compose ps
```

**Prerequisites:** Docker Desktop, a configured Google Cloud project, BigQuery permissions, and the required environment variables and credentials.


## Project Status

The local environment is running, with Airflow and Metabase operational. End-to-end ingestion and dbt model execution are still being validated.

Built as part of my journey in **Data Engineering and cloud data platforms**.