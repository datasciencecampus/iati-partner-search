import numpy as np
import pandas as pd
from os.path import join
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import time
from gensim.models import Word2Vec
import operator

try:
    from ips_python.utils import get_data_path
    from ips_python.preprocessing import preprocess_query_text
    from ips_python.constants import (
        PROCESSED_RECORDS_FILENAME,
        TERM_DOCUMENT_MATRIX_FILENAME,
        VECTORIZER_FILENAME,
        MODEL_NAME,
        WORD_LIST_FILENAME,
    )
except ModuleNotFoundError:
    from utils import get_data_path
    from preprocessing import preprocess_query_text
    from constants import (
        PROCESSED_RECORDS_FILENAME,
        TERM_DOCUMENT_MATRIX_FILENAME,
        VECTORIZER_FILENAME,
        MODEL_NAME,
        WORD_LIST_FILENAME,
    )


# get data ready into lists
def list_for_wordtovec(cdf, qdf):
    f_vectorlist = [row["description"].split(" ") for index, row in cdf.iterrows()]
    # append query
    f_vectorlist.append(str(qdf["description"][0]).split(" "))
    return f_vectorlist


# set up embeddings model
def getwordmodel(pdata, psize, pwindow, pmin):
    return Word2Vec(pdata, size=psize, window=pwindow, min_count=pmin)


# get word vectors
def getwordvectors(pmodel):
    return list(pmodel.wv.vocab)


# put embeddings into a df with words as rownames
def embeddings_in_df(pmodel, pwords):
    # empty df ready to populate
    f_dfvectors = pd.DataFrame(np.zeros((len(pwords), 50)))
    # put embeddings into df
    for row in range(len(pwords)):
        f_dfvectors.loc[row] = np.array([list(pmodel.wv[pwords[row]])])
    # add in the words as rownames
    f_dfvectors.index = pwords
    return f_dfvectors


def embeddings_for_qry(pvectorlist, pvectors, pwords):

    f_qryvector = []
    f_wordsinqry = []
    f_qry = []

    for i in pvectorlist[-1]:
        if i in pwords:
            f_qryvector.append(pvectors.loc[i])
            f_wordsinqry.append(i)
    f_qry.append(f_qryvector)
    f_qry.append(f_wordsinqry)

    return f_qry


# for every vector in qryvector is compared to every value in word vectors
def cosine_res(pdfvector, pqryvector):
    f_similarwords = {}
    for index, value in enumerate(pqryvector):
        for index2, value2 in pdfvector.iterrows():
            cos_result = cosine_similarity(
                np.array(value).reshape(1, value.shape[0]),
                np.array(value2).reshape(1, value2.shape[0]),
            )
            if cos_result > 0.9:
                f_similarwords[index2] = round(float(cos_result), 5)
    f_similarwords = sorted(
        f_similarwords.items(), key=operator.itemgetter(1), reverse=True
    )
    return f_similarwords


def final_rank(psimilarwords, word_list, tdm, df):

    rankings = []
    ids = []
    words = []
    for wrds in psimilarwords:
        pd.Series()
        if wrds[0] in set(word_list):

            colData = tdm[:, word_list.index(wrds[0])].toarray()
            for i in df[colData > 0]["iati.identifier"].tolist():
                ids.append(i)
                words.append(wrds[0])
            for r in colData[colData > 0]:
                rankings.append(r)

    return pd.DataFrame(data={"iati.identifier": ids, "rank": rankings, "word": words})


if __name__ == "__main__":

    start = time.time()

    query = """Despite impressive improvements in Vietnam's development and
    health status over the past decade, gains have not been equitable and significant unmet
    health needs remain. Poor and marginalized populations continue to disproportionally
    suffer from preventable illnesses while those in wealthier socioeconomic groups
    continue to enjoy greater health and longer life expectancy. Social Marketing for
    Improved Rural Health will include 3 main components: i) social marketing of SafeWat
    household water treatment solution and promotion of safer hygiene behaviors; ii) Good
    health, Great life and iii) behavior change communication to address non-supply side
    barriers to healthier behaviors."""

    # get clean data for embeddings
    clean_df = pd.read_csv(
        join(get_data_path(), PROCESSED_RECORDS_FILENAME), encoding="utf-8"
    )
    # preprocessing on both query and raw IATI description data
    query_df = preprocess_query_text(query)

    # unpickling
    with open(join(get_data_path(), TERM_DOCUMENT_MATRIX_FILENAME), "rb") as _file:
        term_document_matrix = pickle.load(_file)

    with open(join(get_data_path(), VECTORIZER_FILENAME), "rb") as _file:
        vectorizer = pickle.load(_file)

    with open(join(get_data_path(), WORD_LIST_FILENAME), "rb") as _file:
        word_list = pickle.load(_file)

    vectorlist = list_for_wordtovec(clean_df, query_df)

    # test of all functions
    model = getwordmodel(vectorlist, 50, 5, 20)

    # save embeddings model
    model.wv.save_word2vec_format(MODEL_NAME)
    words = getwordvectors(model)

    dfvectors = embeddings_in_df(model, getwordvectors(model))

    r_qry = embeddings_for_qry(vectorlist, dfvectors, words)

    qryvector = r_qry[0]
    wordsinqry = r_qry[1]

    similarwords = cosine_res(dfvectors, qryvector)

    final = final_rank(similarwords, word_list, term_document_matrix, clean_df)

    final.sort_values(["rank"], inplace=True, ascending=False)

    end = time.time()

    print("completed in {0} seconds".format(end - start))
