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

with engine.connect() as connection:
    result=connection.execute(
        text("""
            SELECT
                MIN(order_purchase_timestamp)::DATE AS start_date,
                MAX(order_purchase_timestamp)::DATE AS end_date
            FROM stg_orders
        """))
    start_date,end_date=result.fetchone()

print(start_date)
print(end_date)

dates=pd.date_range(
    start=start_date,
    end=end_date
    )

date_data=pd.DataFrame(
    {"full_date":dates}
    )

date_data["date_key"]=(date_data["full_date"].dt.strftime("%Y%m%d").astype(int))

date_data["day"]=date_data["full_date"].dt.day
date_data["month"]=date_data["full_date"].dt.month
date_data["quarter"]=date_data["full_date"].dt.quarter
date_data["year"]=date_data["full_date"].dt.year
date_data["month_name"]=date_data["full_date"].dt.month_name()
date_data["day_of_week"]=date_data["full_date"].dt.dayofweek +1
date_data["day_name"]=date_data["full_date"].dt.day_name()

print(date_data.head())
date_data=date_data[
    [ 
        "date_key",
        "full_date",
        "day",
        "month",
        "month_name",
        "quarter",
        "year",
        "day_of_week",
        "day_name"
    ]
]
with engine.begin() as connection:
    connection.execute(
        text("DROP TABLE IF EXISTS dim_date")
    )

    connection.execute(
        text("""
            CREATE TABLE dim_date(
            date_key INTEGER PRIMARY KEY,
            full_date DATE,
            day INTEGER,
            month INTEGER,
            quarter INTEGER,
            year INTEGER,
            month_name TEXT,
            day_of_week INTEGER,
            day_name TEXT
            )
        """)
    )

date_data.to_sql(
    name="dim_date",
    con=engine,
    if_exists="append",
    index=False
)


with engine.connect() as connection:
    result = connection.execute(
        text("""
            SELECT
                COUNT(*) AS total_rows,
                COUNT(DISTINCT date_key) AS unique_keys,
                MIN(full_date),
                MAX(full_date)
            FROM dim_date
        """)
    )

    print(result.fetchone())