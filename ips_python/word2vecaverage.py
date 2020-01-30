import pandas as pd
import numpy as np
from os.path import join
from gensim.models import Word2Vec
import pickle
import time

try:
    from ips_python.utils import get_data_path
    from ips_python.constants import (
        WORD2VECMODEL_FILENAME,
        PROCESSED_RECORDS_FILENAME,
        WORD2VECAVG_FILENAME,
        DESCRIPTION_COLUMN_NAME,
    )
except ModuleNotFoundError:
    from utils import get_data_path
    from constants import (
        WORD2VECMODEL_FILENAME,
        PROCESSED_RECORDS_FILENAME,
        WORD2VECAVG_FILENAME,
        DESCRIPTION_COLUMN_NAME,
    )


def average_per_doc(description_text, w2v_model, dim_size=300):
    description_list = description_text.split(" ")
    mean_array = np.zeros((dim_size,), dtype="float32")
    all_words = set(w2v_model.wv.vocab)
    n_words = 0
    for w in description_list:
        if w in all_words:
            mean_array = np.add(mean_array, w2v_model.wv.get_vector(w))
            n_words += 1
    if n_words > 0:
        mean_array = np.divide(mean_array, n_words)
    return mean_array


def results_per_corpus_df(input_df, w2v_model, dim_size=300):
    results_arr = []
    progress = set([i for i in range(10 ** 5, 10 ** 6, 10 ** 5)])
    for index, row in input_df.iterrows():
        results_arr.append(
            average_per_doc(row[DESCRIPTION_COLUMN_NAME], w2v_model, dim_size)
        )
        if index in progress:
            print("processed {0} records".format(index))
    return np.array(results_arr)


if __name__ == "__main__":

    df1 = pd.read_csv(
        join(get_data_path(), PROCESSED_RECORDS_FILENAME), encoding="utf-8"
    )

    df1 = df1[[DESCRIPTION_COLUMN_NAME]]

    model = Word2Vec.load(join(get_data_path(), WORD2VECMODEL_FILENAME))

    # This takes a while
    start = time.time()
    results = results_per_corpus_df(df1, model, 300)

    with open(join(get_data_path(), WORD2VECAVG_FILENAME), "wb") as output_file:
        pickle.dump(results, output_file)

    print("average array created and saved in {0} seconds".format(time.time() - start))
