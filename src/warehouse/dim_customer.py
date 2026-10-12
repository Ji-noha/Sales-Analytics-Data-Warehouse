from sqlalchemy import create_engine
from sqlalchemy import text
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# local(python/windows) use 5433 as port  and localhost , when using airflow+docker use 5432 and postgres
user=os.getenv("POSTGRES_USER")
password=os.getenv("POSTGRES_PASSWORD")
database=os.getenv("POSTGRES_DB")
port=5432

connection_url= f"postgresql://{user}:{password}@postgres:{port}/{database}"

engine=create_engine(connection_url)

#read customers data from staging table stg_customers

customers=pd.read_sql(
    """ 
    SELECT 
        customer_id,
        customer_unique_id,
        customer_zip_code_prefix,
        customer_city,
        customer_state
    FROM stg_customers
    """,
    engine
)

#surrogate_key

customers["customer_key"]= customers.index +1

print("customer_data:")
print(customers.head())
print(customers.shape)

#create dim table:

with engine.begin() as connection:
    connection.execute(
        text("DROP TABLE IF EXISTS dim_customer")
    )
    connection.execute(
        text("""
            CREATE TABLE dim_customer(
            customer_key INTEGER PRIMARY KEY,
            customer_id TEXT,
            customer_unique_id TEXT,
            customer_zip_code_prefix INTEGER,
            customer_city TEXT,
            customer_state TEXT
            )
            """
        )
    )

print("Dimension table is created")

#load data into dim_customer

customers.to_sql(
    name="dim_customer",
    con=engine,
    if_exists="append",
    index=False
)

with engine.connect() as connection:
    result= connection.execute(
        text("""
            SELECT 
                COUNT(*) AS total_rows,
                COUNT(DISTINCT customer_key) AS unique_keys
            FROM dim_customer
        """)
    )

print(result.fetchone())