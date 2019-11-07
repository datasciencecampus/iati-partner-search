from utils import get_data_path
from preprocessing import preprocess_query_text
from cosine import get_cosine_similarity
import pandas as pd
import numpy as np
from os.path import join
from gensim.models import Word2Vec

from constants import PROCESSED_RECORDS_FILENAME, COSINE_FILENAME


def build_w2v_model(input_df, dim_size):
    vectorlist = [row["description"].split(" ") for index, row in input_df.iterrows()]
    return Word2Vec(vectorlist, min_count=20, size=dim_size, workers=4)


def average_per_doc(description_text, w2v_model):
    description_list = description_text.split(" ")
    mean_array = np.zeros((50,), dtype="float32")
    all_words = set(w2v_model.wv.vocab)
    n_words = 0
    for w in description_list:
        if w in all_words:
            mean_array = np.add(mean_array, w2v_model.wv.get_vector(w))
            n_words += 1
    if n_words > 0:
        mean_array = np.divide(mean_array, n_words)
    return mean_array


def results_per_corpus_df(input_df, dim_size, w2v_model):
    results_arr = np.empty([0, dim_size])
    for index, row in df1.iterrows():
        results_arr = np.vstack(
            (results_arr, average_per_doc(row["description"], w2v_model))
        )
    return results_arr


if __name__ == "__main__":

    query = """Despite impressive improvements in Vietnam's development and
        health status over the past decade, gains have not been equitable and significant unmet
        health needs remain. Poor and marginalized populations continue to disproportionally
        suffer from preventable illnesses while those in wealthier socioeconomic groups
        continue to enjoy greater health and longer life expectancy. Social Marketing for
        Improved Rural Health will include 3 main components: i) social marketing of SafeWat
        household water treatment solution and promotion of safer hygiene behaviors; ii) Good
        health, Great life and iii) behavior change communication to address non-supply side
        barriers to healthier behaviors."""

    df1 = pd.read_csv(
        join(get_data_path(), PROCESSED_RECORDS_FILENAME), encoding="iso-8859-1"
    )

    # On laptop need to limit DF for reasonable performance
    df1 = df1.head(10000)

    model = build_w2v_model(df1, 50)

    # This takes a while
    full_arr_average = results_per_corpus_df(df1, 50, model)

    query_df = preprocess_query_text(query)
    query_average = average_per_doc(str(query_df["description"]), model).reshape(1, -1)

    # Using get_cosine_similarity from our cosine.py script, it removes cosine < 0 results
    out_df = get_cosine_similarity(query_average, full_arr_average, df1)

    out_df.to_csv(
        join(get_data_path(), COSINE_FILENAME), index=False, encoding="iso-8859-1"
    )
