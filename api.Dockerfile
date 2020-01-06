FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./requirements.txt requirements.txt
COPY ips_python/ ips_python/
COPY tasks.py ./tasks.py

COPY data/all_downloaded_records.csv data/all_downloaded_records.csv
COPY data/processed_records.csv data/processed_records.csv
COPY data/vectorizer.pkl data/vectorizer.pkl
COPY data/term_document_matrix.pkl data/term_document_matrix.pkl
COPY data/word_list.pkl data/word_list.pkl

RUN apt-get update &&  \
    # required for numpy
    apt-get --assume-yes install build-essential && \
    pip install --upgrade pip && \
    pip install invoke && \
    invoke install-dependencies && \
    invoke download-nltk-data

ENV APP_MODULE="ips_python.fast_api_app:app"
