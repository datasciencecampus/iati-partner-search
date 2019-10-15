import pickle
from utils import get_data_path
from sklearn.feature_extraction.text import TfidfVectorizer

INTERIM_DATA_WORD_LIST = "wordList.pkl"


def vectorize(path_to_preprocessed_file):
    # Build document-term matrix
    # replace with min_proportion variable if wish
    vectorizer = TfidfVectorizer(min_df=0)
    X = vectorizer.fit_transform(df1["description"])

    # write out the list of words to pickle file
    word_list = vectorizer.get_feature_names()
    with open(
        os.path.join(get_data_path(), INTERIM_DATA_WORD_LIST), "wb"
    ) as output_file:
        pickle.dump(word_list, output_file)

    # Write X to pickle file
    with open(
        os.path.join(get_data_path(), INTERIM_DATA_TERM_DOCUMENT_MATRIX), "wb"
    ) as output_file:
        pickle.dump(X, output_file)


if __name__ == "__main__":
    # example calling of function for script
    pass
