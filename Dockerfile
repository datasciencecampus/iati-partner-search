FROM python:3.7

COPY . /iati-partner-search

WORKDIR /iati-partner-search

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install ipython black flake8

# download the data we need from NLTK
RUN python -c "import nltk; nltk.download('stopwords'); nltk.download('words')"

CMD ["bash"]