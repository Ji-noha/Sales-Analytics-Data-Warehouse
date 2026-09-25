FROM python:3.11-slim

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir kafka-python==3.0.11

RUN pip install --no-cache-dir psycopg2-binary==2.9.13