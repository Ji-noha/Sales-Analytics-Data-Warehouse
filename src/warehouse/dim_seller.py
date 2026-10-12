from sqlalchemy import create_engine
from sqlalchemy import text
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

user=os.getenv("POSTGRES_USER")
password=os.getenv("POSTGRES_PASSWORD")
database=os.getenv("POSTGRES_DB")
port=5432

connection_url= f"postgresql://{user}:{password}@postgres:{port}/{database}"

engine=create_engine(connection_url)

#read customers data from staging table stg_customers

sellers=pd.read_sql(
    """ 
    SELECT 
        seller_id,
        seller_zip_code_prefix,
        seller_city,
        seller_state
    FROM stg_sellers
    """,
    engine
)

#surrogate_key

sellers["seller_key"]= sellers.index +1

print("seller_data:")
print(sellers.head())
print(sellers.shape)

#create dim table:

with engine.begin() as connection:
    connection.execute(
        text("DROP TABLE IF EXISTS dim_seller")
    )
    connection.execute(
        text("""
            CREATE TABLE dim_seller(
            seller_key INTEGER PRIMARY KEY,
            seller_id TEXT,
            seller_zip_code_prefix INTEGER,
            seller_city TEXT,
            seller_state TEXT
            )
            """
        )
    )

print("Dimension table is created")

#load data into dim_seller

sellers.to_sql(
    name="dim_seller",
    con=engine,
    if_exists="append",
    index=False
)

with engine.connect() as connection:
    result= connection.execute(
        text("""
            SELECT 
                COUNT(*) AS total_rows,
                COUNT(DISTINCT seller_key) AS unique_keys
            FROM dim_seller
        """)
    )

print(result.fetchone())