import pickle
from os.path import join
import pandas as pd
import datetime

from typing import List
from fastapi import FastAPI, Query
from pydantic import BaseModel

try:
    from ips_python.utils import get_data_path
    from ips_python.script import process_query
    from ips_python.constants import (
        VECTORIZER_FILENAME,
        TERM_DOCUMENT_MATRIX_FILENAME,
        PROCESSED_RECORDS_FILENAME,
        INPUT_DATA_FILENAME,
    )
except ModuleNotFoundError:
    from utils import get_data_path
    from script import process_query
    from constants import (
        VECTORIZER_FILENAME,
        TERM_DOCUMENT_MATRIX_FILENAME,
        PROCESSED_RECORDS_FILENAME,
        INPUT_DATA_FILENAME,
    )


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


def get_cosine_results(query):
    return process_query(
        query,
        vectorizer,
        term_document_matrix,
        processed_iati_records,
        full_iati_records,
    ).to_dict("records")


app = FastAPI(
    title="IATI Search API", description="Search IATI description data", version="0.1",
)


class IATIQuery(BaseModel):
    # the "..." argument to Query makes search_method a required field
    search_method: str = Query(
        ...,
        regex="(cosine|elastic)",
        example="cosine",
        description=(
            "Select whether the method for search should use the custom-built"
            "cosine solution or use elasticsearch."
        ),
    )
    query: str = Query(
        ...,
        description="Search terms, or description of desired activity.",
        example=(
            "Despite impressive improvements in Vietnam's development and health status "
            "over the past decade, gains have not been equitable and significant unmet "
            "health needs remain. Poor and marginalized populations continue to "
            "disproportionally suffer from preventable illnesses while those in "
            "wealthier socioeconomic groups continue to enjoy greater health and longer "
            "life expectancy. Social Marketing for Improved Rural Health will include 3 "
            "main components: i) social marketing of SafeWat household water treatment "
            "solution and promotion of safer hygiene behaviors; ii) Good health, Great "
            "life and iii) behavior change communication to address non-supply side "
            "barriers to healthier behaviors"
        ),
    )


class IATIResult(BaseModel):
    iati_identifier: str = Query(..., example="XM-DAC-12345-abcde")
    reporting_org: str = Query(..., example="XM-DAC-12345")
    title: str = Query(..., example="Title of An Example Activity")
    description: str = Query(
        ..., example="Delivery of vaccinations to eradicate rabies."
    )
    processed_description: str = Query(
        None,  # passing "None" to Query makes this an optional field
        description=(
            "This is what the description data looks like before it is"
            "vectorized. This is included in order to better understand"
            "what words are included and excluded in the text"
            "preprocessing data."
            ""
            "Not included when using Elasticsearch."
        ),
        example="turkey transit institut build year eu strategi turkey prioriti axe polit criteria civil societi dialogu support vaccin rabi",
    )


class IATIQueryResponse(IATIQuery):
    timestamp: str = Query(
        ..., example="1576247043.016017", description="Unix UTC timestamp"
    )
    version: str = Query(
        ...,
        example="0.1.0",
        description="In reference to what model and data was used.",
    )
    processed_query: str = Query(
        None,  # make this field optional
        description=(
            "The text value that is submitted to the model after preprocessing."
            ""
            "Not included when using Elasticsearch."
        ),
    )
    results: List[IATIResult]


@app.post("/search", response_model=IATIQueryResponse)
def search_iati_post(iati_query: IATIQuery):
    timestamp = datetime.datetime.utcnow().timestamp()
    # model and stuff goes here . . .
    return {
        "search_method": "cosine",
        "query": "Delivery of vaccinations to eradicate rabies.",
        "timestamp": timestamp,
        "version": "0.1.0",
        "processed_query": "deliveri erad rabi",
        "results": [
            {
                "iati_identifier": "XI-IATI-EC_NEAR-2010/22518/17",
                "reporting_org": "XI-IATI-EC_NEAR",
                "title": "Oral Vaccination against Rabies",
                "description": "National programme for Turkey under the IPA - Transition Assistance and Institution Building Component for the year 2010.To support the EU pre-accession strategy for Turkey under 4 priority axes: Copenhagen political criteria, acquis communautaire, EU-Turkey Civil Society Dialogue and supporting activities.Oral Vaccination against Rabies",
                "processed_description": "turkey transit institut build year eu strategi turkey prioriti axe polit criteria civil societi dialogu support vaccin rabi",
            }
        ],
    }
