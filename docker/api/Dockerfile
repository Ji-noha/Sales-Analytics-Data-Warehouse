FROM python:3.11-slim

WORKDIR /app

COPY src  /app/src

RUN pip install --no-cache-dir --default-timeout=300  --retries=5 fastapi uvicorn

RUN pip install --no-cache-dir --default-timeout=300  --retries=5 psycopg2-binary

RUN pip install --no-cache-dir --default-timeout=300 --retries=5 sqlalchemy

RUN pip install --no-cache-dir  --default-timeout=300 --retries=5  python-dotenv

CMD ["python" ,"-m" ,"uvicorn" ,"src.api.main:app" ,"--reload","--host","0.0.0.0"]