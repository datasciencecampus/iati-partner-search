FROM python:3.7

COPY . /iati-partner-search

WORKDIR /iati-partner-search

RUN pip install --upgrade pip && \
    pip install invoke && \
    invoke install-dependencies && \
    invoke download-nltk-data

ENV FLASK_APP app/main.py

EXPOSE 5000

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
