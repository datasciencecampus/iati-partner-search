import pickle
from os.path import join
import pandas as pd
from utils import get_data_path
from sklearn.feature_extraction.text import TfidfVectorizer

from constants import (
    PROCESSED_RECORDS_FILENAME,
    WORD_LIST_FILENAME,
    TERM_DOCUMENT_MATRIX_FILENAME,
    VECTORIZER_FILENAME,
)


def create_tfidf_term_document_matrix(
    preprocessed_file_name,
    word_list_file_name,
    term_document_matrix_filename,
    vectorizer_filename,
):
    # read in the csv
    df1 = pd.read_csv(
        join(get_data_path(), preprocessed_file_name), encoding="iso-8859-1"
    )

    df1 = df1[["iati.identifier", "description"]]
    # Build document-term matrix
    # replace with min_proportion variable if wish
    vectorizer = TfidfVectorizer(min_df=0)
    X = vectorizer.fit_transform(df1["description"])

    # write out the list of words to pickle file
    word_list = vectorizer.get_feature_names()
    with open(join(get_data_path(), word_list_file_name), "wb") as output_file:
        pickle.dump(word_list, output_file)

    # Write X to pickle file
    with open(
        join(get_data_path(), term_document_matrix_filename), "wb"
    ) as output_file:
        pickle.dump(X, output_file)
    # Write vectorizer to pickle file
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
    print(type(vectorizer))
    return vectorizer.transform(processed_query_dataframe["description"])


if __name__ == "__main__":
    create_tfidf_term_document_matrix(
        PROCESSED_RECORDS_FILENAME,
        WORD_LIST_FILENAME,
        TERM_DOCUMENT_MATRIX_FILENAME,
        VECTORIZER_FILENAME,
    )
