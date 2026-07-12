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