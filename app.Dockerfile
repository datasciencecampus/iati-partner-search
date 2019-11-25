FROM python:3.7

COPY /app /iati-partner-search/app
COPY /python /iati-partner-search/python
COPY /data /iati-partner-search/data
COPY /input /iati-partner-search/input
COPY requirements.txt /iati-partner-search

WORKDIR /iati-partner-search

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install ipython black flake8

# download the data we need from NLTK
RUN python -c "import nltk; nltk.download('stopwords'); nltk.download('words')"

ENV FLASK_APP app/main.py 

EXPOSE 5000

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]