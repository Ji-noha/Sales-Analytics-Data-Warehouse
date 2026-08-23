# POSTGRESQL
===
docker-compose.yml 
docker compose up -d 
2- docker ps (see if the conatiner is working)
3- if postgresql in docker RUN docker exec -it postgres psql -U postgres -d ecommerce
If everything works, you'll see:

ecommerce=#

🎉 You're now inside PostgreSQL.

4- SELECT current_database(); 
it will show you that you are in ecommerce db

5- SELECT current_user; 
it will show postgres as your user
6- SELECT schema_name
FROM information_schema.schemata;

it will show you schemas

7- CREATE SCHEMA raw;

CREATE SCHEMA analytics;

8- in sql file write all CREATE TABLE ...
9- psql --version

10-inside psql 
#postgres
CREATE DATABASE ecommerce;
11- \l (you will see db as ecommerce , postgres)

12- inside psql do _c ecommerce
(now you are in the ecommerce db ecommerce=#)

Why did this happen?

Earlier you were connecting with:

docker exec -it postgres psql -U postgres -d ecommerce

That command connects inside the Docker container.

Now you're connecting with:

psql -h localhost ...

That connects to whatever PostgreSQL server is listening on your computer.

# ERROR & solution
postgres=# \l 'more' is not recognized as an internal or external command, operable program or batch file.
is not a PostgreSQL error. It means psql is trying to use the Windows more program as a pager, but it can't find it.

First, disable the pager

Inside psql, run:

\pset pager off

13- RUN SELECT current_database();
(it gives postgres 1row)

14- SELECT datname
FROM pg_database;
(to see the database)

14- RUN docker ps ( if you see postgres that means you are connecting to postgres in docker)

15- create shemas inside ecommerce
CREATE SCHEMA raw;
CREATE SCHEMA analytics;

16-IN TERMINAL bash NOT IN PSQL (ecommerce=#)

psql -h localhost -U postgres -d ecommerce -f sql/02_create_raw_tables.sql

17- INSIDE PSQL 
\dt raw.* 
(you will see tables)
18- TO INSPECT ONE TABLE DO : 
\d raw.orders
(you will see columns of this table)


#Dictionary → len(dictionary)
List → len(list)

"""
    Reads all CSV files from the data folder.

    Returns:
        dict: Dictionary where
            key = dataset name
            value = pandas DataFrame
"""
Python lets us compress that exact loop into:

missing_required = [
    column for column in required
    if column not in df.columns
]

The pattern is:

[result for item in collection if condition]


df[column] = pd.to_datetime(
    df[column],
    errors="coerce"
)

means:

"Try to convert every value into a date. If something cannot be converted, don't crash; replace it with NaT."

For example:

"2018-01-10 10:30:00"  →  2018-01-10 10:30:00 ✅
"2018-02-15 14:20:00"  →  2018-02-15 14:20:00 ✅
NaN                    →  NaT                  ✅
"hello"                →  NaT                  ⚠️

NaT means Not a Time.

It's the datetime equivalent of NaN.

# stem works with just a file path , if we want name from datset usr replace("want to remove", "to put instead")



## PostgreSQL + Docker: Python connected to the wrong PostgreSQL instance

### Problem

I successfully connected Python/SQLAlchemy to PostgreSQL and `to_sql()` reported success:

Database connection is successful  
Starting customers load...  
Customers load finished!

Python could also see the table:

[('public', 'stg_customers')]

However, when checking PostgreSQL through Docker:

docker exec -it postgres psql -U postgres -d ecommerce -c "\dt"

I got:

Did not find any relations.

This was confusing because Python said that `stg_customers` existed.

### Diagnosis

The problem was that there were two PostgreSQL instances competing for the PostgreSQL port 5432.

Python was connecting to a PostgreSQL instance on:

localhost:5432

while the PostgreSQL instance inside the Docker container was a different instance.

Therefore:

Python → PostgreSQL instance A → stg_customers
Docker → PostgreSQL instance B → no tables

The important lesson is that a successful database connection does not automatically mean that I am connected to the database instance I intended.

### Useful commands

Check the Docker container:

docker ps

Check the port exposed by the Docker container:

docker port postgres

Expected:

5432/tcp -> 0.0.0.0:5432

Connect directly to PostgreSQL inside Docker:

docker exec -it postgres psql -U postgres -d ecommerce

List tables:

\dt

Check the current database:

SELECT current_database();

Check the current user:

SELECT current_user;

### Debugging from Python

# """ the debugging code
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from .transform import datasets
from sqlalchemy import text

load_dotenv()
user=os.getenv("POSTGRES_USER")
password=os.getenv("POSTGRES_PASSWORD")
database=os.getenv("POSTGRES_DB")
port= 5432

database_url=f"postgresql://{user}:{password}@localhost:{port}/{database}"

engine=create_engine(database_url)

engine = create_engine(database_url)

print("DATABASE:", database)
print("USER:", user)
print("URL:", database_url.replace(password, "****"))

with engine.connect() as connection:
    result = connection.execute(
        text("SELECT current_database(), current_user;")
    )
    print(result.fetchone())

    result = connection.execute(
        text("""
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """)
    )
    print(result.fetchall())

print("Starting customers load...")

datasets["olist_customers_dataset"].to_sql(
    name="stg_customers",
    con=engine,
    if_exists="replace",
    index=False
)

print("Customers load finished!")

for name, df in datasets.items():
    table_name="stg_"+ name.replace("olist_","").replace("_dataset","")
    df.to_sql(
    name=table_name,
    con=engine,
    if_exists="replace",
    index=False
)
# """
SQLAlchemy can be used to verify the database connection:

from sqlalchemy import text

with engine.connect() as connection:
    result = connection.execute(
        text("SELECT current_database(), current_user;")
    )
    print(result.fetchone())

We can also check which tables Python can see:

with engine.connect() as connection:
    result = connection.execute(
        text("""
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """)
    )
    print(result.fetchall())

### Solution

I checked the Windows services and found that another PostgreSQL service was running.

I stopped the local PostgreSQL service so that Docker could use port 5432.
===
went to services.msc in pc and stop postgre...

Then I restarted the Docker database:

docker compose down
docker compose up -d

After that, Python and Docker were using the same PostgreSQL instance.

### Final verification

Run the ETL loader:

python -m src.load

Then verify from Docker:

docker exec -it postgres psql -U postgres -d ecommerce

List the tables:

\dt

The staging table should appear:

stg_customers

Then verify the number of rows:

SELECT COUNT(*) FROM stg_customers;

Expected:

99441

### Engineering lesson

When debugging database connections, don't only ask:

"Can I connect?"

Also ask:

"Which database server am I actually connected to?"

A database connection has several important pieces:

Host
Port
User
Password
Database

With Docker, I also need to consider whether another database service is already using the same host port.

The general debugging workflow is:

Application
    ↓
Connection configuration
    ↓
Host + Port
    ↓
Database server
    ↓
Database
    ↓
Table
    ↓
Data

Always verify each layer instead of assuming that a successful connection means everything is correct.

Important concept:

localhost:5432 is an endpoint, not a guarantee that I'm talking to the PostgreSQL instance I intended.

#
datasets.items() → gives you dataset name + DataFrame
to_sql() → can create the table automatically
if_exists="replace" → full refresh
localhost:5432 → host/port connection
.env → keeps credentials outside the code
SQLAlchemy → connects Python to PostgreSQL
stg_ → identifies staging tables
the difference between a source dataset name and a database table name
## ==
STAGING
──────────────
Pandas can create the table
        ↓
to_sql()
        ↓
simple storage
## ==
WAREHOUSE
────────────────────────
1. Design schema
        ↓
2. CREATE TABLE
        ↓
3. Define PK/FK/types
        ↓
4. to_sql(..., append)
        ↓
5. Load data
## ===
6. So to_sql() has two jobs depending on how we use it
Option A — Let Pandas create the table
df.to_sql(
    "dim_product",
    engine,
    if_exists="replace",
    index=False
)

Pandas:

CREATE TABLE
      +
INSERT

Easy, but less control.

Option B — We create the table ourselves
with engine.begin() as connection:
    connection.execute(
        text("""
            CREATE TABLE dim_product (
                product_key INTEGER PRIMARY KEY,
                product_id TEXT,
                ...
            )
        """)
    )

Then:

df.to_sql(
    "dim_product",
    engine,
    if_exists="append",
    index=False
)

Now:

                 PostgreSQL
                     │
        ┌────────────┴────────────┐
        │                         │
 CREATE TABLE                  to_sql
 schema definition              rows
        │                         │
        └────────────┬────────────┘
                     ↓
              dim_product

This is the approach we're practicing.
## =====
engine = create_engine(database_url)

The engine is basically SQLAlchemy's database communication/connection-management object.

A transaction is basically:

A group of database operations that should succeed together or be rolled back together.
with engine.begin() as connection:

is useful.

It gives you a connection inside a transaction and automatically commits if everything succeeds.

start transaction
      ↓
execute SQL
      ↓
if successful → commit
if error → rollback

That's a very useful production habit.

connect()
with engine.connect() as connection:

You're saying:

"Give me a database connection so I can interact with the database."

Good for things like:

SELECT ...

especially when you're just reading.

begin()
with engine.begin() as connection:

You're saying:

"I'm going to perform operations as a transaction."

Useful for:

CREATE TABLE
INSERT
UPDATE
DELETE
ALTER TABLE

and multiple related operations

The three options
Option	What happens
fail	Error if table exists
replace	Drop/recreate table
append	Keep table and add rows

## 
ocker exec -it postgres psql -U postgres -d ecommerce   
psql (16.14 (Debian 16.14-1.pgdg13+1))
Type "help" for help.

ecommerce=# DROP TABLE IF EXISTS dim_product;
NOTICE:  table "dim_product" does not exist, skipping
DROP TABLE

## ========
SQLAlchemy → ecommerce → dim_product → 32,951 rows ✅

while:

docker exec ... psql → "dim_product does not exist" ❌

That means they are almost certainly not talking to the same PostgreSQL instance/data, despite both appearing to use port 5432.

The clue is especially strong because your Python connection reported:

::1:5432

while Docker port mapping can expose the container on the host. We need to identify exactly what PostgreSQL each client is reaching.

Let's stop guessing
1. From Python, run this
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

You'll get something like:

('ecommerce', 'postgres', '::1', 5432, 'PostgreSQL ...')
2. Now use Docker to ask the container itself

Run:

docker exec -it postgres psql -U postgres -d ecommerce -c "SELECT current_database(), current_user, inet_server_addr(), inet_server_port(), version();"

Then:

docker exec -it postgres psql -U postgres -d ecommerce -c "\dt"
Why this matters

We need to compare:

Python / SQLAlchemy
        ↓
     PostgreSQL A ?

Docker exec
        ↓
     PostgreSQL B ?

If the version() or server address differs, we've found the problem.

There is another possibility: your Docker container has a PostgreSQL server, but your Windows machine also has PostgreSQL installed/running, and Python is connecting to the Windows PostgreSQL through localhost:5432 rather than the Docker one.

That would perfectly explain the weird behavior you've been seeing.

For example:

Python
  ↓
localhost:5432
  ↓
Windows PostgreSQL
  ↓
dim_product exists


docker exec
  ↓
postgres container
  ↓
different PostgreSQL
  ↓
dim_product doesn't exist

And this is exactly why engineers verify the actual server identity, not just the hostname and port.

#
Windows
   │
   │ localhost:5433
   ▼
Docker PostgreSQL 16
   │
   │ :5432 internally
   ▼
ecommerce
   ├── dim_product
   ├── ...
   └── future fact tables


##
 python src\warehouse\dim_customer.py
customer_data:
                        customer_id  ... customer_key
0  06b8999e2fba1a1fbc88172c00ba8bc7  ...            1
1  18955e83d337fd6b2def6b18a428ac77  ...            2
2  4e7b3e00288586ebd08712fdd0374a03  ...            3
3  b2b6027bc5c5109e529d4dc6358b12c3  ...            4
4  4f2d8ab171c80ec8364f7c12e35b23ad  ...            5

[5 rows x 6 columns]
(99441, 6)
Dimension table is created
(99441, 99441)
PS C:\Users\user\Sales Analytics Data Warehouse> docker exec -it postgres psql -U postgres -d ecommerce -c "SELECT COUNT(*), COUNT(DISTINCT customer_key) FROM dim_customer;"
 count | count 
-------+-------
 99441 | 99441
(1 row)

#

MIN(order_purchase_timestamp)::DATE

converts the timestamp to a date.
##
stg_orders
    ↓
MIN/MAX dates
    ↓
start_date / end_date
    ↓
pd.date_range()
    ↓
DatetimeIndex
    ↓
pd.DataFrame()
    ↓
date_data
    ↓
add date attributes
    ↓
dim_date