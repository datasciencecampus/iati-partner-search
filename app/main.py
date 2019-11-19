import sys

sys.path.append("./python/")

import os, json
from flask import Flask, request, render_template
from script import process_query
from constants import (
    VECTORIZER_FILENAME,
    TERM_DOCUMENT_MATRIX_FILENAME,
    PROCESSED_RECORDS_FILENAME,
    INPUT_DATA_FILENAME,
)
import pickle
from os.path import join
from utils import get_data_path
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

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


@app.route("/")
@app.route("/search")
def home():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    search_term = request.form["search"]
    search_method = request.form["search-method"]

    if search_method == "cosine":
        results = process_query(
            search_term,
            vectorizer,
            term_document_matrix,
            processed_iati_records,
            full_iati_records,
        ).to_dict('records')

        return render_template("results.html", results=results)

    elif search_method == "elastic":
        url = os.getenv('ELASTICSEARCH_URL') + "/_search"
        payload = {
            "query": {
                "more_like_this": {
                    "fields": ["title", "description"],
                    "like": search_term,
                    "min_term_freq": 1,
                    "max_query_terms": 30,
                }
            }
        }
        headers = {"Content-Type": "application/json"}

        response = requests.get(url, data=json.dumps(payload), headers=headers).json()
        results = response['hits']['hits']
        return render_template("elastic-results.html", results=results)

    else:
        return "sorry, you need to specify a search method"


if __name__ == "__main__":
    app.run(debug=True)
