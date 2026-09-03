from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
import pandas as pd
from sqlalchemy import text

load_dotenv()

user=os.getenv("POSTGRES_USER")
password=os.getenv("POSTGRES_PASSWORD")
database=os.getenv("POSTGRES_DB")
port=5432

database_url= f"postgresql://{user}:{password}@postgres:{port}/{database}"

engine=create_engine(database_url)

sales=pd.read_sql(
    """
    SELECT
        oi.order_id,
        oi.order_item_id,
        oi.product_id,
        oi.seller_id,
        oi.shipping_limit_date,
        oi.price,
        oi.freight_value,
        oi.total_sales,
        o.customer_id,
        o.order_purchase_timestamp,
        p.product_key,
        s.seller_key,
        c.customer_key,
        d.date_key
        FROM stg_order_items AS oi
        JOIN stg_orders AS o
            ON oi.order_id = o.order_id
        LEFT JOIN dim_product AS p
            ON oi.product_id = p.product_id
        LEFT JOIN dim_seller AS s
            ON oi.seller_id = s.seller_id
        LEFT JOIN dim_customer AS c
            ON o.customer_id = c.customer_id
        LEFT JOIN dim_date AS d
            ON o.order_purchase_timestamp::DATE =d.full_date
    """, 
    engine       
)

"""
print(sales[["product_key", "seller_key", "customer_key", "date_key"]].isna().sum())
print(sales.head())
print(sales[["customer_id", "customer_key"]].head())
print(sales[["order_purchase_timestamp", "date_key"]].head())
print(sales.shape)
"""
sales_fact = sales[[
    "order_id",
    "order_item_id",
    "customer_key",
    "product_key",
    "seller_key",
    "date_key",
    "shipping_limit_date",
    "price",
    "freight_value",
    "total_sales"
]]

sales_fact["sales_key"] = sales_fact.index + 1

sales_fact = sales_fact[[
    "sales_key",
    "order_id",
    "order_item_id",
    "customer_key",
    "product_key",
    "seller_key",
    "date_key",
    "shipping_limit_date",
    "price",
    "freight_value",
    "total_sales"
]]


with engine.begin() as connection:
    connection.execute(text("DROP TABLE IF EXISTS fact_sales"))

    connection.execute(
        text("""
            CREATE TABLE fact_sales(
                sales_key INTEGER PRIMARY KEY,
                order_id  TEXT,
                order_item_id INTEGER,
                customer_key INTEGER,
                product_key INTEGER,
                seller_key INTEGER,
                date_key INTEGER,
                shipping_limit_date TIMESTAMP,
                price DOUBLE PRECISION,
                freight_value DOUBLE PRECISION,
                total_sales DOUBLE PRECISION
            )
        """)
    )

sales_fact.to_sql(
    name="fact_sales",
    con=engine,
    if_exists="append",
    index=False
)

with engine.connect() as connection:
    result = connection.execute(
        text("""
            SELECT
                COUNT(*) AS total_rows,
                COUNT(DISTINCT sales_key) AS unique_sales_keys,
                SUM(total_sales) AS total_revenue
            FROM fact_sales
        """)
    )

    print(result.fetchone())

with engine.connect() as connection:
    result=connection.execute(
        text("""
            SELECT 
                COUNT (*) AS total_rows,
                COUNT (*) FILTER (WHERE product_key is NULL ) AS missing_products,
                COUNT (*) FILTER (WHERE seller_key is NULL ) AS missing_sellers,
                COUNT (*) FILTER (WHERE customer_key is NULL ) AS missing_customer,
                COUNT (*) FILTER (WHERE date_key is NULL ) AS missing_dates
            FROM fact_sales
        """)
    )

    print(result.fetchone())

with engine.connect() as connection:
    result = connection.execute(
        text("""
            SELECT
                COUNT(*) AS total_rows,
                COUNT(DISTINCT (order_id, order_item_id)) AS unique_order_items
            FROM fact_sales
        """)
    )

    print(result.fetchone())

