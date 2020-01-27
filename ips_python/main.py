import os
import json
import random
import string
import datetime

from flask import Flask, request, render_template
from flask.views import MethodView
from flask_smorest import Api, Blueprint
from ips_python.schemas import IATIQuery, IATIQueryResponse

from ips_python.script import process_query, process_query_embeddings
from ips_python.constants import (
    VECTORIZER_FILENAME,
    TERM_DOCUMENT_MATRIX_FILENAME,
    PROCESSED_RECORDS_FILENAME,
    INPUT_DATA_FILENAME,
    WORD2VECMODEL_FILENAME,
    WORD2VECAVG_FILENAME,
    ELASTICSEARCH_INDEX_NAME,
    TITLE_COLUMN_NAME,
    DESCRIPTION_COLUMN_NAME,
    IATI_IDENTIFIER_COLUMN_NAME,
    ORG_ID_COLUMN_NAME,
)
import pickle
from os.path import join, dirname
from ips_python.utils import get_data_path
import pandas as pd
from dotenv import load_dotenv

from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, RadioField, SubmitField
from wtforms.validators import DataRequired
from elasticsearch import Elasticsearch


dotenv_path = join(dirname(dirname(__file__)), ".env")
load_dotenv(dotenv_path)

environment = os.getenv("FLASK_ENV", "development").lower()

app = Flask(__name__)
app.config["OPENAPI_URL_PREFIX"] = "/openapi"
app.config["OPENAPI_JSON_PATH"] = "openapi.json"
app.config["OPENAPI_REDOC_PATH"] = "/doc/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger/"
app.config["OPENAPI_SWAGGER_UI_VERSION"] = "3.23.11"
app.config["OPENAPI_VERSION"] = "3.0.2"
openapi = Api(app)

if environment == "production":
    app.secret_key = os.getenv("APP_SECRET_KEY")
else:
    app.secret_key = "".join(random.choice(string.ascii_lowercase) for i in range(10))

with open(join(get_data_path(), VECTORIZER_FILENAME), "rb") as _file:
    vectorizer = pickle.load(_file)

with open(join(get_data_path(), TERM_DOCUMENT_MATRIX_FILENAME), "rb") as _file:
    term_document_matrix = pickle.load(_file)

with open(join(get_data_path(), WORD2VECMODEL_FILENAME), "rb") as _file:
    word_to_vec_model = pickle.load(_file)

with open(join(get_data_path(), WORD2VECAVG_FILENAME), "rb") as _file:
    word_to_vec_document_average = pickle.load(_file)

processed_iati_records = pd.read_csv(
    join(get_data_path(), PROCESSED_RECORDS_FILENAME), encoding="iso-8859-1"
)

full_iati_records = pd.read_csv(
    join(get_data_path(), INPUT_DATA_FILENAME), encoding="iso-8859-1"
)


class SearchForm(FlaskForm):
    search_method = RadioField(
        "Search method: ",
        choices=[
            ("cosine", "Cosine Similarity"),
            ("elastic", "Elasticsearch"),
            ("embeddings", "Embeddings"),
        ],
        default="cosine",
    )
    search = TextAreaField("Query:", validators=[DataRequired()])
    submit = SubmitField("Search")

    class Meta:
        csrf = False


def get_elasticsearch_results(query):
    elasticsearch_url = os.getenv("ELASTICSEARCH_URL")
    elasticsearch_instance = Elasticsearch([elasticsearch_url])
    payload = {
        "query": {
            "more_like_this": {
                "fields": [TITLE_COLUMN_NAME, DESCRIPTION_COLUMN_NAME],
                "like": query,
                "min_term_freq": 1,
                "max_query_terms": 30,
            }
        }
    }

    response = elasticsearch_instance.search(
        index=ELASTICSEARCH_INDEX_NAME, body=json.dumps(payload)
    )
    return response["hits"]["hits"]


def get_cosine_results(query):
    return process_query(
        query,
        vectorizer,
        term_document_matrix,
        processed_iati_records,
        full_iati_records,
    ).to_dict("records")


def get_embeddings_results(query):
    return process_query_embeddings(
        query,
        word_to_vec_model,
        word_to_vec_document_average,
        processed_iati_records,
        full_iati_records,
    ).to_dict("records")


@app.route("/", methods=["POST", "GET"])
# @app.route("/search")
def home():
    form = SearchForm(request.form)
    from pprint import pprint

    pprint(dir(form.search))
    if request.method == "POST":
        if form.validate():
            results = None
            search_type = form.data["search_method"]
            if search_type == "cosine":
                results = get_cosine_results(form.data["search"])
            elif search_type == "embeddings":
                results = get_embeddings_results(form.data["search"])
            else:
                results = get_elasticsearch_results(form.data["search"])
            return render_template(
                "index.html", form=form, results=results, result_type=search_type
            )
    return render_template("index.html", form=form)


# ------------------------------------- Start: OpenAPI Set Up -------------------------------------
# Set up the OpenAPI access
api_blueprint = Blueprint("api", "api", url_prefix="/api", description="IATI Search")

example_query = {
    "search_method": "cosine",
    "query": "Delivery of vaccinations to eradicate rabies.",
}

example_response = {
    **example_query,
    "timestamp": datetime.datetime.utcnow().timestamp(),
    # TODO: implement versioning feature
    # "version": "0.1.0",
    "processed_query": "deliveri erad rabi",
    "results": [
        {
            "iati_identifier": "XI-IATI-EC_NEAR-2010/22518/17",
            "reporting_org": "XI-IATI-EC_NEAR",
            "title": "Oral Vaccination against Rabies",
            "description": "National programme for Turkey under the IPA - Transition Assistance and Institution Building Component for the year 2010.To support the EU pre-accession strategy for Turkey under 4 priority axes: Copenhagen political criteria, acquis communautaire, EU-Turkey Civil Society Dialogue and supporting activities.Oral Vaccination against Rabies",
            "processed_description": "turkey transit institut build year eu strategi turkey prioriti axe polit criteria civil societi dialogu support vaccin rabi",
        },
        {
            "iati_identifier": "XI-IATI-EC_NEAR-2010/22518/17",
            "reporting_org": "XI-IATI-EC_NEAR",
            "title": "Oral Vaccination against Rabies",
            "description": "National programme for Turkey under the IPA - Transition Assistance and Institution Building Component for the year 2010.To support the EU pre-accession strategy for Turkey under 4 priority axes: Copenhagen political criteria, acquis communautaire, EU-Turkey Civil Society Dialogue and supporting activities.Oral Vaccination against Rabies",
            "processed_description": "turkey transit institut build year eu strategi turkey prioriti axe polit criteria civil societi dialogu support vaccin rabi",
        },
    ],
}


def transform_result(result):
    """
    Transform a dict of an IATI result to API result

    We change the mappings of the IATI.cloud column
    names to the ones we have deinfed in our API.
    This works for cosine and embeddings approaches
    but it does not work for elasticsearch as we need
    to transform the mappings from the elasticsearch API
    """
    return {
        "iati_identifier": result[IATI_IDENTIFIER_COLUMN_NAME],
        "reporting_org": result[ORG_ID_COLUMN_NAME],
        "title": result[TITLE_COLUMN_NAME],
        "description": result[DESCRIPTION_COLUMN_NAME],
    }


@api_blueprint.route("/search")
class Search(MethodView):
    @api_blueprint.arguments(IATIQuery, example=example_query)
    @api_blueprint.response(IATIQueryResponse, example=example_response)
    def post(self, query_data):
        timestamp = datetime.datetime.utcnow().timestamp()

        search_type = query_data["search_method"]
        query = query_data["query"]

        iati_results = []
        if search_type == "cosine":
            results = get_cosine_results(query)
            iati_results = [transform_result(result) for result in results]

        elif search_type == "embeddings":
            results = get_embeddings_results(query)
            iati_results = [transform_result(result) for result in results]

        elif search_type == "elastic":
            results = get_elasticsearch_results(query)
            iati_results = [
                {
                    "iati_identifier": result["_source"][IATI_IDENTIFIER_COLUMN_NAME],
                    "reporting_org": result["_source"][ORG_ID_COLUMN_NAME],
                    "title": result["_source"][TITLE_COLUMN_NAME],
                    "description": result["_source"][DESCRIPTION_COLUMN_NAME],
                }
                for result in results
            ]
        else:
            raise Exception("Improper Request")  # TODO: add proper exception from Flask

        return {
            "search_method": search_type,
            "query": query,
            "timestamp": timestamp,
            "results": iati_results,
        }


openapi.register_blueprint(api_blueprint)

# ------------------------------------- End: OpenAPI Set Up -------------------------------------

if __name__ == "__main__":
    if environment == "development":
        app.run(debug=True)
    elif environment == "production":
        app.run(debug=False)
