import sys

sys.path.append("./python/")

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
    results = process_query(
        search_term,
        vectorizer,
        term_document_matrix,
        processed_iati_records,
        full_iati_records,
    ).to_html()
    return render_template("results.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)

