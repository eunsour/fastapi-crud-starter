FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

COPY ./requirements.txt /app/requirements.txt

RUN apt-get update && \
    apt-get -y install gcc libmariadb-dev && \
    pip install --upgrade pip

COPY ./app /app