FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY . /iati-partner-search
WORKDIR /iati-partner-search

RUN apt-get update &&  \
    # required for numpy
    apt-get --assume-yes install build-essential && \
    pip install --upgrade pip && \
    pip install invoke && \
    invoke install-dependencies && \
    invoke download-nltk-data

ENV APP_MODULE="ips_python.fast_api_app:app"
