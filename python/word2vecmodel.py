from utils import get_data_path
import pandas as pd
from os.path import join
from gensim.models import Word2Vec
import time

from constants import PROCESSED_RECORDS_FILENAME, WORD2VECMODEL_FILENAME

def build_w2v_model(input_df, dim_size):
    vectorlist = [row["description"].split(" ") for index, row in input_df.iterrows()]
    return Word2Vec(vectorlist, min_count=20, size=dim_size, workers=4)


if __name__ == "__main__":
    

    df1 = pd.read_csv(
        join(get_data_path(), PROCESSED_RECORDS_FILENAME), encoding="iso-8859-1"
    )
    
    start = time.time()
    model = build_w2v_model(df1, 50)
    
    model.save(join(get_data_path(), WORD2VECMODEL_FILENAME))
    
    print("saved w2v model in {0} seconds".format(time.time() - start))