import sys

sys.path.append("./python/")

import os
import json
import random
import string

from flask import Flask, request, render_template
from script import process_query
from constants import (
    VECTORIZER_FILENAME,
    TERM_DOCUMENT_MATRIX_FILENAME,
    PROCESSED_RECORDS_FILENAME,
    INPUT_DATA_FILENAME,
)
import pickle
from os.path import join, dirname
from utils import get_data_path
import pandas as pd
import requests
from dotenv import load_dotenv

from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, RadioField, SubmitField
from wtforms.validators import DataRequired


dotenv_path = join(dirname(dirname(__file__)), ".env")
load_dotenv(dotenv_path)

environment = os.getenv("FLASK_ENV", "development").lower()

app = Flask(__name__)
if environment == "production":
    app.secret_key = os.getenv("APP_SECRET_KEY")
else:
    app.secret_key = "".join(random.choice(string.ascii_lowercase) for i in range(10))

with open(join(get_data_path(), VECTORIZER_FILENAME), "rb") as _file:
    vectorizer = pickle.load(_file)

with open(join(get_data_path(), TERM_DOCUMENT_MATRIX_FILENAME), "rb") as _file:
    term_document_matrix = pickle.load(_file)

processed_iati_records = pd.read_csv(
    join(get_data_path(), PROCESSED_RECORDS_FILENAME), encoding="iso-8859-1"
)

full_iati_records = pd.read_csv(
    join(get_data_path(), INPUT_DATA_FILENAME), encoding="iso-8859-1"
)


class SearchForm(FlaskForm):
    search_method = RadioField(
        "Search method: ",
        choices=[("cosine", "Cosine Similarity"), ("elastic", "Elasticsearch")],
        default="cosine",
    )
    search = TextAreaField("Query:", validators=[DataRequired()])
    submit = SubmitField("Search")

    class Meta:
        csrf = False


def get_elasticsearch_results(query):
    url = os.getenv("ELASTICSEARCH_URL") + "/_search"
    payload = {
        "query": {
            "more_like_this": {
                "fields": ["title", "description"],
                "like": query,
                "min_term_freq": 1,
                "max_query_terms": 30,
            }
        }
    }
    headers = {"Content-Type": "application/json"}

    response = requests.get(url, data=json.dumps(payload), headers=headers).json()
    return response["hits"]["hits"]


def get_cosine_results(query):
    return process_query(
        query,
        vectorizer,
        term_document_matrix,
        processed_iati_records,
        full_iati_records,
    ).to_dict("records")


@app.route("/", methods=["POST", "GET"])
# @app.route("/search")
def home():
    form = SearchForm(request.form)
    if request.method == "POST":
        if form.validate():
            results = None
            search_type = form.data["search_method"]
            if search_type == "cosine":
                results = get_cosine_results(form.data["search"])
            else:
                results = get_elasticsearch_results(form.data["search"])
            return render_template(
                "index.html", form=form, results=results, result_type=search_type
            )
    return render_template("index.html", form=form)


if __name__ == "__main__":
    if environment == "development":
        app.run(debug=True)
    elif environment == "production":
        app.run(debug=False)
