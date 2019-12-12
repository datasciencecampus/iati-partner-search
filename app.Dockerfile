FROM python:3.7

COPY . /iati-partner-search

WORKDIR /iati-partner-search

<<<<<<< HEAD
RUN pip install --upgrade pip && \
    pip install invoke && \
    invoke install-dependencies && \
=======
RUN pip install --upgrade pip &&
    pip install invoke &&
    invoke install-dependencies &&
>>>>>>> Update Docker build and setup
    invoke download-nltk-data

ENV FLASK_APP app/main.py

EXPOSE 5000

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
