from unittest import TestCase
from os.path import join, dirname, abspath
import pandas as pd

from ips_python.preprocessing import preprocess_pipeline
from ips_python.vectorize import create_tfidf_term_document_matrix
from ips_python.script import process_query

INPUT_DATA_FILENAME = "sample_test_data.csv"


def get_test_data_file():
    return join(dirname(abspath(__file__)), "test_data")


class TestPipeline(TestCase):
    def test_pipeline_basic(self):
        """
        Test that the preprocessing of data and vectorizing works without errors

        Must produce 4 outputs:
            - processed_df
            - vectorizer
            - term_document_matrix
            - word_list

        These are all used at 'runtime' to process a user query
        """
        raw_data = pd.read_csv(
            join(get_test_data_file(), INPUT_DATA_FILENAME), encoding="iso-8859-1"
        )

        # preprocessing
        processed_df = preprocess_pipeline(raw_data)

        # assumptions about the data
        # check number of rows
        assert processed_df.shape[0] > 0

        vectorizer, term_document_matrix, word_list = create_tfidf_term_document_matrix(
            processed_df
        )

        assert vectorizer is not None
        assert term_document_matrix is not None
        assert word_list is not None

    def test_runtime_basic(self):
        # setup
        raw_data = pd.read_csv(
            join(get_test_data_file(), INPUT_DATA_FILENAME), encoding="iso-8859-1"
        )
        processed_df = preprocess_pipeline(raw_data)
        vectorizer, term_document_matrix, word_list = create_tfidf_term_document_matrix(
            processed_df
        )

        # run time query
        query = """Despite impressive improvements in Vietnam's development and
            health status over the past decade, gains have not been equitable and significant unmet
            health needs remain. Poor and marginalized populations continue to disproportionally
            suffer from preventable illnesses while those in wealthier socioeconomic groups
            continue to enjoy greater health and longer life expectancy. Social Marketing for
            Improved Rural Health will include 3 main components: i) social marketing of SafeWat
            household water treatment solution and promotion of safer hygiene behaviors; ii) Good
            health, Great life and iii) behavior change communication to address non-supply side
            barriers to healthier behaviors."""

        results = process_query(
            query_text=query,
            vectorizer=vectorizer,
            term_document_matrix=term_document_matrix,
            processed_iati_records=processed_df,
            full_iati_records=raw_data,
        )

        assert results is not None
