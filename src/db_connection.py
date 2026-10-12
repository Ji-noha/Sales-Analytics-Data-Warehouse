from sqlalchemy import  engine
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
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
                current_database(),
                current_user,
                inet_server_addr(),
                inet_server_port(),
                version()
        """)
    )
    print(result.fetchone())

with engine.connect() as connection:
    result = connection.execute(
        text("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
    )

    for row in result:
        print(row[0])