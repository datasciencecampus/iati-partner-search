from unittest import TestCase
from os.path import join, dirname, abspath
import pandas as pd

from python.preprocessing import preprocess_pipeline
from python.vectorize import create_tfidf_term_document_matrix

INPUT_DATA_FILENAME = "sample_test_data.csv"


def get_test_data_file():
    return join(dirname(abspath(__file__)), "test_data")


class TestPipeline(TestCase):
    def test_pipeline_basic(self):
        # get the test data
        raw_data = pd.read_csv(
            join(get_test_data_file(), INPUT_DATA_FILENAME), encoding="iso-8859-1"
        )

        # preprocessing
        processed_df = preprocess_pipeline(raw_data)

        # assumptions about the data
        # check number of rows
        assert processed_df.shape[0] > 0

        vectorizer, term_document_matrix, word_list = create_tfidf_term_document_matrix(processed_df)

        assert vectorizer is not None
        assert term_document_matrix is not None
        assert word_list is not None

    def test_pipeline_complicated(self):
        # test the data path
        pass
