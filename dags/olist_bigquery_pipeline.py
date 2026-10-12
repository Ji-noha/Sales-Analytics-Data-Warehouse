from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import sys
sys.path.append("/opt/airflow/src")
from files_discovery import discover_files
from google.cloud import bigquery


with DAG(
        dag_id="olist_bigquery_pipeline",
        start_date=datetime(2026, 1, 1),
        schedule=None,
        catchup=False,
) as dag:
        @task
        def discover_csv():
                return discover_files()       
        files=discover_csv()
        @task(
                retries=3,
                retry_delay=timedelta(minutes=2)
        )
        def load_file(file_info):
                dataset_name="olist_raw"
                file_path = "/opt/airflow/data/raw/" + file_info["file"]
                table_name = file_info["table"]

                connection = bigquery.Client(project="southern-shade-469107-i6")
                table_id = connection.project + "." + dataset_name + "." + table_name

                job_config = bigquery.LoadJobConfig()
                job_config.allow_quoted_newlines=True
                job_config.source_format=bigquery.SourceFormat.CSV
                job_config.skip_leading_rows = 1
                job_config.autodetect = True
                job_config.write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
                with open(file_path,"rb") as file:
                        job=connection.load_table_from_file(file,table_id,job_config=job_config)
                        job.result()
                print(job.output_rows)

        load_tasks= load_file.expand(file_info=files)

        build=BashOperator(
                task_id="build_dbt",
                bash_command= "cd /opt/airflow/dbt/olist_analytics && dbt build --exclude fact_sales "
        )

load_tasks >> build

        