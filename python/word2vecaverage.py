from utils import get_data_path
import pandas as pd
import numpy as np
from os.path import join
from gensim.models import Word2Vec
import pickle
from constants import WORD2VECMODEL_FILENAME, PROCESSED_RECORDS_FILENAME, WORD2VECAVG_FILENAME
import time

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


def results_per_corpus_df(input_df, w2v_model, avg_filename, dim_size=300):
    results_arr = []
    progress = set([i for i in range(100000, 1000000, 100000)])
    for index, row in input_df.iterrows():
        results_arr.append(average_per_doc(row["description"], w2v_model, dim_size))
        if index in progress:
            print("processed {0} records".format(index))
    results_arr = np.array(results_arr)    
    with open(join(get_data_path(), avg_filename), "wb") as output_file:
        pickle.dump(results_arr, output_file)
    

if __name__ == "__main__":
    
    df1 = pd.read_csv(
        join(get_data_path(), PROCESSED_RECORDS_FILENAME), encoding="iso-8859-1"
    )
    
    df1 = df1[['description']]

    model = Word2Vec.load(join(get_data_path(), WORD2VECMODEL_FILENAME))

    # This takes a while
    start = time.time()
    results_per_corpus_df(df1, model, WORD2VECAVG_FILENAME, 300)
    print("average array created in {0} seconds".format(time.time()- start))