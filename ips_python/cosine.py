import time
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from ips_python.utils import get_data_path
from os.path import join

try:
    from ips_python.preprocessing import preprocess_query_text
    from ips_python.vectorize import vectorize_input_text
    from ips_python.constants import (
        PROCESSED_RECORDS_FILENAME,
        TERM_DOCUMENT_MATRIX_FILENAME,
        VECTORIZER_FILENAME,
        COSINE_FILENAME,
    )
except ModuleNotFoundError:
    from preprocessing import preprocess_query_text
    from vectorize import vectorize_input_text
    from constants import (
        PROCESSED_RECORDS_FILENAME,
        TERM_DOCUMENT_MATRIX_FILENAME,
        VECTORIZER_FILENAME,
        COSINE_FILENAME,
    )


def get_cosine_similarity(
    processed_user_query_vector, term_document_matrix, iati_records
):
    """
    input:
        TDM
        IATI Records used in TDM
        vectorized query

    output:
        cosine similarity > 0 per iati.identifier
    """

    cosine_array = cosine_similarity(term_document_matrix, processed_user_query_vector)

    iati_records = iati_records[["iati.identifier"]]

    iati_records["cosine_sim"] = cosine_array

    # Remove all non-zero results?
    iati_records = iati_records[iati_records["cosine_sim"] > 0]

    return iati_records


if __name__ == "__main__":

    # Test query
    query = """Despite impressive improvements in Vietnam's development and
    health status over the past decade, gains have not been equitable and significant unmet
    health needs remain. Poor and marginalized populations continue to disproportionally
    suffer from preventable illnesses while those in wealthier socioeconomic groups
    continue to enjoy greater health and longer life expectancy. Social Marketing for
    Improved Rural Health will include 3 main components: i) social marketing of SafeWat
    household water treatment solution and promotion of safer hygiene behaviors; ii) Good
    health, Great life and iii) behavior change communication to address non-supply side
    barriers to healthier behaviors."""

    # Or uncomment below if wish to test input text at runtime
    # query = input("Please enter search text:\n")

    query_df = preprocess_query_text(query)

    if not query_df.empty:
        with open(join(get_data_path(), VECTORIZER_FILENAME), "rb") as _file:
            vectorizer = pickle.load(_file)
        query_vector = vectorize_input_text(query_df, vectorizer)

        with open(join(get_data_path(), TERM_DOCUMENT_MATRIX_FILENAME), "rb") as _file:
            term_document_matrix = pickle.load(_file)

        iati_records = pd.read_csv(
            join(get_data_path(), PROCESSED_RECORDS_FILENAME), encoding="iso-8859-1"
        )

        iati_records = iati_records[["iati.identifier"]]
        start_time = time.time()
        outDF = get_cosine_similarity(query_vector, term_document_matrix, iati_records)
        print("cosine match in {0} seconds".format(time.time() - start_time))
        # example calling of function for script
        # cosine_similar("tdm.pkl", "vec.pkl", "iati_records", "")

        outDF.to_csv(
            join(get_data_path(), COSINE_FILENAME), index=False, encoding="iso-8859-1"
        )
    else:
        print("no words exist after pre-processing")
