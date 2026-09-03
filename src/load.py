import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from transform import datasets

load_dotenv()

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
database = os.getenv("POSTGRES_DB")
port = 5432

database_url = f"postgresql://{user}:{password}@postgres:{port}/{database}"

engine = create_engine(database_url)

for name, df in datasets.items():
    table_name = "stg_" + name.replace("olist_", "").replace("_dataset", "")

    print(f"Loading {name} → {table_name}, rows={len(df)}")
    
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="replace",
        index=False
    )