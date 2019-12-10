import sys
import os
from os.path import join, dirname

import json
import string
import pickle
import logging

import pandas as pd
import requests

from flask import Flask, request, render_template, jsonify, Blueprint
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, RadioField, SubmitField
from wtforms.validators import DataRequired
from flask_restplus import Api, Resource, fields

# ensure that ips_python module is accessible
sys.path.append(os.path.abspath(os.path.dirname("__file__")))

from ips_python.utils import get_data_path
from ips_python.script import process_query
from ips_python.constants import (
    VECTORIZER_FILENAME,
    TERM_DOCUMENT_MATRIX_FILENAME,
    PROCESSED_RECORDS_FILENAME,
    INPUT_DATA_FILENAME,
)

import settings

log = logging.getLogger(__name__)

log.info("Reading in vectorizer")
with open(join(get_data_path(), VECTORIZER_FILENAME), "rb") as _file:
    vectorizer = pickle.load(_file)

log.info("Reading in TDM")
with open(join(get_data_path(), TERM_DOCUMENT_MATRIX_FILENAME), "rb") as _file:
    term_document_matrix = pickle.load(_file)

log.info("Reading in processed IATI records")
processed_iati_records = pd.read_csv(
    join(get_data_path(), PROCESSED_RECORDS_FILENAME), encoding="iso-8859-1"
)

log.info("Reading in full IATI records")
full_iati_records = pd.read_csv(
    join(get_data_path(), INPUT_DATA_FILENAME), encoding="iso-8859-1"
)

flask_app = Flask(__name__)
api = Api(flask_app, version='1.0', title='IATI Partner Search',
    description='TODO',
)
search_query = api.model("Search Query", {
    "search_method": fields.String(Required=True, description="Method for search - either 'cosine' or 'elasticsearch"),
    "search": fields.String(Required=True, description="Description of project")
})


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


@flask_app.route("/", methods=["POST", "GET"])
# @flask_app.route("/search")
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
            from pprint import pprint
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            pprint(request.headers)
            if "Content-type" in request.headers and request.headers["Content-type"] == "application/json":
                return jsonify(results)
            return render_template(
                "index.html", form=form, results=results, result_type=search_type
            )
    return render_template("index.html", form=form)


def configure_app(flask_app):
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def initialize_app(flask_app):
    pass


namespace = api.namespace('search', description='search operations')
search_query = api.model("Search Query", {
    "search_method": fields.String(Required=True, description="Method for search - either 'cosine' or 'elasticsearch"),
    "search": fields.String(Required=True, description="Description of project")
})


@namespace.route('/api')
class Search(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''

    @namespace.doc('search_query')
    @namespace.expect(search_query)
    @namespace.marshal_with(search_query, code=200)
    def post(self):
        '''Create a new task'''
        return {"search_method":"something", "search": "another_thing"}, 200



def main():
    configure_app(flask_app)

    # FLASK RESTful API Set up
    # blueprint = Blueprint('api', __name__, url_prefix='/api')
    # api.init_app(blueprint)

    # flask_app.register_blueprint(blueprint)

    # change the .env file to enable or disable debugging
    flask_app.run(debug=settings.FLASK_DEBUG)

if __name__ == "__main__":
    main()
