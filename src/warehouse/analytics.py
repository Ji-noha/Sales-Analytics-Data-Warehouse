from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
import pandas as pd
from sqlalchemy import text

load_dotenv()

user=os.getenv("POSTGRES_USER")
password=os.getenv("POSTGRES_PASSWORD")
database=os.getenv("POSTGRES_DB")
port=5433

database_url= f"postgresql://{user}:{password}@localhost:{port}/{database}"

engine=create_engine(database_url)

with engine.connect() as connection:
    result = connection.execute(
        text("""
            SELECT
                SUM(total_sales) AS total_revenue,
                COUNT(DISTINCT order_id) AS number_orders,
                COUNT(order_item_id) AS number_order_items,
                COUNT(DISTINCT customer_key) AS number_customers,
                SUM(total_sales) / COUNT(DISTINCT order_id) AS average_order_value,
                AVG(price) AS average_item_price
            FROM fact_sales;
            """))
    print(result.fetchone())
    
    result = connection.execute(
        text(""" 
            SELECT
                d.year,
                SUM(f.total_sales) AS revenue
            FROM fact_sales AS f
            JOIN dim_date AS d
                    ON f.date_key = d.date_key
            GROUP BY d.year
            ORDER BY d.year;
            """))
    print(result.fetchall())
    result = connection.execute(
            text("""
            SELECT
                d.year,
                d.month,
                d.month_name,
                SUM(f.total_sales) AS revenue
            FROM fact_sales AS f
            JOIN dim_date AS d
                    ON f.date_key = d.date_key
            GROUP BY d.year, d.month, d.month_name
            ORDER BY d.year, d.month;
            """))
    print(result.fetchall())
    result = connection.execute(
            text("""
            SELECT
                p.product_category_name_english AS category,
                SUM(f.total_sales) AS revenue
            FROM fact_sales AS f
            JOIN dim_product AS p
                ON f.product_key = p.product_key
            GROUP BY p.product_category_name_english
            ORDER BY revenue DESC
            LIMIT 10;
        """))
    print(result.fetchall())
    result = connection.execute(
            text("""
            SELECT
                p.product_key,
                p.product_id,
                p.product_category_name_english AS category,
            SUM(f.total_sales) AS revenue
            FROM fact_sales AS f
            JOIN dim_product AS p
                ON f.product_key = p.product_key
            GROUP BY p.product_key, p.product_id, p.product_category_name_english
            ORDER BY revenue DESC
            LIMIT 10;
        """))
    print(result.fetchall())
    result = connection.execute(
            text("""
            SELECT
                s.seller_key,
                s.seller_id,
                s.seller_city,
                s.seller_state,
                SUM(f.total_sales) AS revenue
            FROM fact_sales AS f
            JOIN dim_seller AS s
                ON f.seller_key = s.seller_key
            GROUP BY s.seller_key, s.seller_id, s.seller_city, s.seller_state
            ORDER BY revenue DESC
            LIMIT 10;
        """))
    print(result.fetchall())
    result = connection.execute(
            text("""
            SELECT
                c.customer_state,
                COUNT(DISTINCT f.customer_key) AS number_customers,
                SUM(f.total_sales) AS revenue
            FROM fact_sales AS f
            JOIN dim_customer AS c
                    ON f.customer_key = c.customer_key
            GROUP BY c.customer_state
            ORDER BY revenue DESC;
        """))
    print(result.fetchall())
    result = connection.execute(
            text("""
            SELECT
                d.year,
                d.month,
                p.product_category_name_english AS category,
                SUM(f.total_sales) AS revenue
            FROM fact_sales AS f
            JOIN dim_date AS d
                ON f.date_key = d.date_key
            JOIN dim_product AS p
                ON f.product_key = p.product_key
            GROUP BY
                d.year,
                d.month,
                p.product_category_name_english
            ORDER BY
                d.year,
                d.month,
                revenue DESC;
        """))
    print(result.fetchall())
    result = connection.execute(
            text("""
            SELECT
                c.customer_id,
                SUM(f.total_sales) AS revenue
            FROM fact_sales AS f
            JOIN dim_customer AS c
                ON f.customer_key = c.customer_key
            GROUP BY c.customer_id
            ORDER BY revenue DESC
            LIMIT 10;
        """))
    print(result.fetchall())

    