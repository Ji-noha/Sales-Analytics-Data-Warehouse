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

## Getting Started

Start the services:

```bash id="7xy0sw"
docker compose up -d --build
```

Check their status:

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