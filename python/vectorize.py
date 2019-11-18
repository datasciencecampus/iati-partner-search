import pickle
from os.path import join
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from .utils import get_data_path
from .constants import (
    PROCESSED_RECORDS_FILENAME,
    WORD_LIST_FILENAME,
    TERM_DOCUMENT_MATRIX_FILENAME,
    VECTORIZER_FILENAME,
)


def create_tfidf_term_document_matrix(preprocessed_text_dataframe):
    """
    return a vectorizer object, TFIDF term document matrix and list of words

    input:
        preprocessed_text_dataframe: dataframe of preprocessed text with 'description' column

    output:
        tuple: vectorizer, term_document_matrix, word_list
    """
    vectorizer = TfidfVectorizer(min_df=0)
    term_document_matrix = vectorizer.fit_transform(
        preprocessed_text_dataframe["description"]
    )

    word_list = vectorizer.get_feature_names()

    return (vectorizer, term_document_matrix, word_list)


def write_tfidf_term_document_matrix_to_file(
    preprocessed_file_name,
    word_list_file_name,
    term_document_matrix_filename,
    vectorizer_filename,
):
    df1 = pd.read_csv(
        join(get_data_path(), preprocessed_file_name), encoding="iso-8859-1"
    )
    df1 = df1[["iati.identifier", "description"]]

    vectorizer, term_document_matrix, word_list = create_tfidf_term_document_matrix(df1)

    with open(
        join(get_data_path(), term_document_matrix_filename), "wb"
    ) as output_file:
        pickle.dump(term_document_matrix, output_file)

    with open(join(get_data_path(), word_list_file_name), "wb") as output_file:
        pickle.dump(word_list, output_file)

    with open(join(get_data_path(), vectorizer_filename), "wb") as output_file:
        pickle.dump(vectorizer, output_file)


def vectorize_input_text(processed_query_dataframe, vectorizer):
    """
    input:
        processed_query_text: dataframe of processed user text
        vectorizer: TfidfVectorizer object

    output:
        numpy array of vectorized user input
    """
    # use the transform method from the vectorizer
    return vectorizer.transform(processed_query_dataframe["description"])


if __name__ == "__main__":
    write_tfidf_term_document_matrix_to_file(
        PROCESSED_RECORDS_FILENAME,
        WORD_LIST_FILENAME,
        TERM_DOCUMENT_MATRIX_FILENAME,
        VECTORIZER_FILENAME,
    )
