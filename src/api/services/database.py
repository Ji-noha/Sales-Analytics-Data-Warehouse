import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

user=os.getenv("POSTGRES_USER")
password=os.getenv("POSTGRES_PASSWORD")
database=os.getenv("POSTGRES_DB")
port=5432

database_url=f"postgresql+psycopg2://{user}:{password}@postgres:{port}/{database}"

engine=create_engine(database_url)

