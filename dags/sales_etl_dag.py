from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
from datetime import timedelta

default_args={
        "retries":2,
        "retry_delay":timedelta(minutes=5),
}

with DAG (
        dag_id="etl_pipeline",
        start_date=datetime(2026,8,31),
        schedule="0 2 * * *",
        default_args=default_args,
        catchup=False,
) as dag:

        extract=BashOperator(
                task_id="extract_csv",
                bash_command="PYTHONPATH=/opt/airflow/src python -m extract",
        )

        transform=BashOperator(
                task_id="transform_data",
                bash_command="PYTHONPATH=/opt/airflow/src python -m transform",
        )

        load=BashOperator(
                task_id="load_data",
                bash_command="PYTHONPATH=/opt/airflow/src python -m load",
        )

        load_customer=BashOperator(
                task_id="dim_customer",
                bash_command="PYTHONPATH=/opt/airflow/src python -m warehouse.dim_customer",
        )

        load_product=BashOperator(
                task_id="dim_product",
                bash_command="PYTHONPATH=/opt/airflow/src python -m warehouse.dim_product",
        )

        load_seller=BashOperator(
                task_id="dim_seller",
                bash_command="PYTHONPATH=/opt/airflow/src python -m warehouse.dim_seller",
        )

        load_date=BashOperator(
                task_id="dim_date",
                bash_command="PYTHONPATH=/opt/airflow/src python -m warehouse.dim_date",
        )

        load_fact=BashOperator(
                task_id="fact_table",
                bash_command="PYTHONPATH=/opt/airflow/src python -m warehouse.fact_table",
        )

        extract >> transform >> load
        load >> [load_customer,load_product,load_seller,load_date] 
        [load_customer,load_product,load_seller,load_date] >> load_fact