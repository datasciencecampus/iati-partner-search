import pandas as pd
import nltk
from os.path import join
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import time

from utils import get_data_path


def preprocess_example(file_path_to_data):
    """preprocessing function.

    Args:
        file_path_to_data: The first parameter.

    Returns:
        A list of strings that have been processed

    """
    print("I am doing something")

    return None


def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {
        "J": wordnet.ADJ,
        "N": wordnet.NOUN,
        "V": wordnet.VERB,
        "R": wordnet.ADV,
    }

    return tag_dict.get(tag, wordnet.NOUN)


def preprocessing_language_detection(p_df, p_text):

    # remove na description values
    p_df = p_df.dropna(subset=[p_text])

    # convert to string:
    p_df = p_df.astype(str)

    # remove punctuation
    p_df[p_text] = p_df[p_text].str.replace(r"[^\w\s]", "")

    # remove underscores not picked up as punctuation above
    p_df[p_text] = p_df[p_text].str.replace("_", "")

    # remove  numbers
    p_df[p_text] = p_df[p_text].str.replace(r"[\d+]", "")

    # lowercase
    p_df[p_text] = p_df[p_text].apply(lambda x: " ".join(x.lower() for x in x.split()))

    # Remove empty string
    p_df = p_df[p_df[p_text] != ""]

    # Remove entirely whitespace strings in description column
    p_df = p_df[~p_df[p_text].str.isspace()]

    # only English language please
    for index, row in p_df.iterrows():
        try:
            if detect(row[p_text]) != "en":
                p_df = p_df.drop(index)
        except Exception:
            # get rid of any garbage
            p_df = p_df.drop(index)

    # remove stopwords English
    stop = stopwords.words("english")
    p_df[p_text] = p_df[p_text].apply(
        lambda x: " ".join(x for x in x.split() if x not in stop)
    )

    # lemmatise text
    lemmatizer = WordNetLemmatizer()
    p_df[p_text] = p_df[p_text].apply(
        lambda x: " ".join(
            [lemmatizer.lemmatize(x, get_wordnet_pos(x)) for x in x.split()]
        )
    )

    return p_df


def preprocessing_eng_only(p_df, p_text):
    start_time = time.time()

    wordstokeep = set(nltk.corpus.words.words())
    stop_words = stopwords.words("english")

    print("completed setup in {0} seconds".format(time.time() - start_time))

    # remove na description values
    p_df = p_df.dropna(subset=[p_text])

    print("completed SETUP in {0} seconds".format(time.time() - start_time))

    # convert to string:
    p_df = p_df.astype(str)

    # remove punctuation
    p_df[p_text] = p_df[p_text].str.replace(r"[^\w\s]", "")

    print("completed REMOVE PUNCTUATION in {0} seconds".format(time.time() - start_time))

    # remove underscores not picked up as punctuation above
    p_df[p_text] = p_df[p_text].str.replace("_", " ")

    print("completed REMOVE UNDERSCORES in {0} seconds".format(time.time() - start_time))

    # remove  numbers
    p_df[p_text] = p_df[p_text].str.replace(r"[\d+]", "")

    print("completed REMOVE NUMBERS in {0} seconds".format(time.time() - start_time))

    # lowercase
    p_df[p_text] = p_df[p_text].apply(lambda x: " ".join(x.lower() for x in x.split()))

    print("completed MAKE LOWERCASE in {0} seconds".format(time.time() - start_time))

    # Remove word if not in English dictionary
    p_df[p_text] = p_df[p_text].apply(
        lambda x: " ".join(x for x in x.split() if x in wordstokeep)
    )

    print(
        "completed REMOVE NON-ENGLISH WORDS in {0} seconds".format(time.time() - start_time)
    )

    # Remove english stop words
    p_df[p_text] = p_df[p_text].apply(
        lambda x: " ".join(x for x in x.split() if x not in stop_words)
    )

    print(
        "completed REMOVE ENGLISH STOP WORDS in {0} seconds".format(time.time() - start_time)
    )

    # Porter stemmer
    st = PorterStemmer()
    p_df[p_text] = p_df[p_text].apply(
        lambda x: " ".join([st.stem(word) for word in x.split()])
    )

    print("completed STEMMING in {0} seconds".format(time.time() - start_time))

    # Remove empty string
    p_df = p_df[p_df[p_text] != ""]

    print("completed REMOVE EMPTY STRINGS in {0} seconds".format(time.time() - start_time))

    # Remove entirely whitespace strings in description column
    p_df = p_df[~p_df[p_text].str.isspace()]

    print("completed REMOVE WHITESPACE in {0} seconds".format(time.time() - start_time))

    return p_df


if __name__ == "__main__":

    start = time.time()

    # set working_directory to path to input files and where outputs will be written (leave blank if same directory as this script)
    INPUT_DATA_FILENAME = "all_downloaded_records.csv"

    INTERIM_DATA_TERM_DOCUMENT_MATRIX = "iatiFullTDM.pkl"
    INTERIM_DATA_USED_RECORDS = "all_used_records_stemEngDict.csv"

    # To import full dataset
    df1 = pd.read_csv(join(get_data_path(), INPUT_DATA_FILENAME), encoding="iso-8859-1")

    df1 = df1[["iati.identifier", "description"]]

    # preprocessing
    df1 = preprocessing_eng_only(df1, "description")

    # write out df with reduced records
    dfout = df1[["iati.identifier", "description"]]
    dfout.to_csv(join(join(get_data_path(), INTERIM_DATA_USED_RECORDS)))

    end = time.time()

    print("completed in {0} seconds".format(end - start))
