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


products=pd.read_sql(
    """
    SELECT 
        p.product_id,
        p.product_category_name,
        p.product_name_lenght,
        p.product_description_lenght,
        p.product_photos_qty,
        p.product_weight_g,
        p.product_length_cm,
        p.product_height_cm,
        p.product_width_cm, 
        c.product_category_name_english 
    FROM stg_products AS p
    LEFT JOIN stg_product_category_name_translation AS c
    ON p.product_category_name=c.product_category_name
    """,
    engine
)

products["product_key"] = products.index + 1


"""
print(products.shape)
print(products.columns)
print(products.head())
print(products.dtypes)
"""


with engine.begin() as connection:
    connection.execute(
        text("DROP TABLE IF EXISTS dim_product")
    )


    connection.execute(
        text("""
            CREATE TABLE dim_product(
            product_key INTEGER PRIMARY KEY,
            product_id  TEXT,
            product_category_name TEXT,
            product_name_lenght INTEGER,
            product_description_lenght INTEGER,
            product_photos_qty INTEGER,
            product_weight_g  DOUBLE PRECISION,
            product_length_cm DOUBLE PRECISION,
            product_height_cm DOUBLE PRECISION,
            product_width_cm DOUBLE PRECISION,
            product_category_name_english TEXT
        )
    """)
)

print("DIMENSION TABLE CREATED")

with engine.connect() as connection:
    result = connection.execute(
        text("""
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_name = 'dim_product'
        """)
    )
    print(result.fetchall())

# first comment that to_sql run , the creation first and then run that code to add data
products.to_sql(
    name="dim_product",
    con=engine,
    if_exists="append",
    index=False
)


with engine.connect() as connection:
    result = connection.execute(
        text("""
            SELECT
                COUNT(*) AS total_rows,
                COUNT(DISTINCT product_key) AS unique_keys
            FROM dim_product
        """)
    )
    print(result.fetchone())


