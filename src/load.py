import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from .transform import datasets

load_dotenv()

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
database = os.getenv("POSTGRES_DB")
port = 5433

database_url = f"postgresql://{user}:{password}@localhost:{port}/{database}"

engine = create_engine(database_url)

for name, df in datasets.items():
    table_name = "stg_" + name.replace("olist_", "").replace("_dataset", "")

    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="replace",
        index=False
    )