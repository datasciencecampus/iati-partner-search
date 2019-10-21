import pandas as pd
import nltk
from os.path import join
from nltk.corpus import stopwords, wordnet
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from langdetect import detect
import time

from utils import get_data_path, get_input_path
from constants import (
    PROCESSED_RECORDS_FILENAME,
    INPUT_DATA_FILENAME,
    STOPWORDS_FILENAME,
)


def preprocessing_initial_text_clean(p_df, p_text):
    # remove na description values
    p_df = p_df.dropna(subset=[p_text])
    # convert to string:
    p_df = p_df.astype(str)
    # remove punctuation
    p_df[p_text] = p_df[p_text].str.replace(r"[^\w\s]", "")
    # remove underscores not picked up as punctuation above
    p_df[p_text] = p_df[p_text].str.replace("_", " ")
    # remove  numbers
    p_df[p_text] = p_df[p_text].str.replace(r"[\d+]", "")
    # lowercase
    p_df[p_text] = p_df[p_text].apply(lambda x: " ".join(x.lower() for x in x.split()))
    return p_df


def preprocessing_nonenglish_paragraph_remove(p_df, p_text):
    # only English language please
    for index, row in p_df.iterrows():
        try:
            if detect(row[p_text]) != "en":
                p_df = p_df.drop(index)
        except Exception:
            # get rid of any garbage
            p_df = p_df.drop(index)
    return p_df


def preprocessing_nonenglish_words_remove(p_df, p_text):
    wordstokeep = set(nltk.corpus.words.words())
    # Remove word if not in English dictionary
    p_df[p_text] = p_df[p_text].apply(
        lambda x: " ".join(x for x in x.split() if x in wordstokeep)
    )
    return p_df


def append_to_stop(stoplist, inputfile):
    with open(inputfile, "r") as r:
        new_words = r.read().splitlines()
        new_words = [w.lower() for w in new_words]
    return stoplist + new_words


def preprocessing_stopwords_remove(p_df, p_text):
    # Remove english stop words
    stop = stopwords.words("english")
    stop = append_to_stop(stop, join(get_input_path(), STOPWORDS_FILENAME))
    p_df[p_text] = p_df[p_text].apply(
        lambda x: " ".join(x for x in x.split() if x not in stop)
    )
    return p_df


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


def preprocessing_lemmatise(p_df, p_text):
    lemmatizer = WordNetLemmatizer()
    p_df[p_text] = p_df[p_text].apply(
        lambda x: " ".join(
            [lemmatizer.lemmatize(x, get_wordnet_pos(x)) for x in x.split()]
        )
    )
    return p_df


def preprocessing_stem(p_df, p_text):
    st = PorterStemmer()
    p_df[p_text] = p_df[p_text].apply(
        lambda x: " ".join([st.stem(word) for word in x.split()])
    )
    return p_df


def preprocessing_empty_text_remove(p_df, p_text):
    # Remove na string
    p_df = p_df[~p_df[p_text].isna()]
    # Remove empty string
    p_df = p_df[p_df[p_text] != ""]
    # Remove entirely whitespace strings in description column
    p_df = p_df[~p_df[p_text].str.isspace()]
    # Remove nan stored as string
    p_df = p_df[p_df[p_text] != "nan"]
    return p_df


def preprocess_query_text(query_text):
    # transform into dataframe
    df = pd.DataFrame([query_text], columns=["description"])
    # Apply specific preprocessing functions
    df = preprocessing_initial_text_clean(df, "description")
    df = preprocessing_nonenglish_words_remove(df, "description")
    df = preprocessing_stopwords_remove(df, "description")
    df = preprocessing_stem(df, "description")
    return preprocessing_empty_text_remove(df, "description")


if __name__ == "__main__":

    start = time.time()

    # To import full dataset
    df1 = pd.read_csv(join(get_data_path(), INPUT_DATA_FILENAME), encoding="iso-8859-1")

    df1 = df1[["iati.identifier", "description", "title"]]

    # Remove record in current full dataset with null iati.identifer
    df1 = df1[~df1["iati.identifier"].str.isspace()]

    # If both description and title not NA concatenate them into description column
    df1.loc[~df1["description"].isna() & ~df1["title"].isna(), ["description"]] = (
        df1["title"] + " " + df1["description"]
    )

    # If description is NA replace with title
    df1.loc[df1["description"].isna(), ["description"]] = df1["title"]

    df1 = df1[["iati.identifier", "description"]]

    # preprocessing
    df1 = preprocessing_initial_text_clean(df1, "description")
    df1 = preprocessing_nonenglish_words_remove(df1, "description")
    df1 = preprocessing_stopwords_remove(df1, "description")
    df1 = preprocessing_stem(df1, "description")
    df1 = preprocessing_empty_text_remove(df1, "description")

    # write out df with reduced records
    df1.to_csv(
        join(join(get_data_path(), PROCESSED_RECORDS_FILENAME)),
        index=False,
        encoding="iso-8859-1",
    )

    end = time.time()

    print("completed in {0} seconds".format(end - start))
