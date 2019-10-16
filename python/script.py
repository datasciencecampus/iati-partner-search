from utils import get_timestamp_string_prefix, get_data_path
from preprocessing import preprocessing_eng_only
from vectorize import create_tfidf_term_document_matrix


def download_data():
    """
    this is a placeholder function to show that we need to run something in order to procure the data
    """
    pass


def main():
    download_data()
    preprocessing_eng_only()
    create_tfidf_term_document_matrix()


def process_query(query_text):
    processed_df = preprocessing_eng_only_query_text(query_text)
    vectorized_query = vectorize_input_text(
        processed_query_dataframe, vectorizer_filename
    )


if __name__ == "__main__":
    main()
