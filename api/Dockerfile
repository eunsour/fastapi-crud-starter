FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

COPY ./requirements.txt /app/requirements.txt

RUN apt-get update && \
    apt-get -y install gcc libmariadb-dev && \
    pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app


# FROM python:3.8

# RUN apt update \
#     && apt install -y default-mysql-client \
#     && apt install --no-install-recommends -y tzdata \
#     && apt clean

# WORKDIR /usr/src/app
# ADD requirements.txt .
# RUN pip install -U pip \
#     && pip install --trusted-host pypi.python.org -r requirements.txt
    
# COPY ./app /app
