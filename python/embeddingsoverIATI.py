# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 10:37:51 2019

@author: s-minhas
"""
import numpy as np
import pandas as pd
from os.path import join
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from os.path import join
from utils import get_data_path
from sklearn.feature_extraction.text import TfidfVectorizer
from preprocessing import *
import time
from utils import get_data_path, get_input_path
from gensim.models import Word2Vec
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
plt.rcParams.update({'font.size': 7})
import operator
from constants import (
    PROCESSED_RECORDS_FILENAME,
    INPUT_DATA_FILENAME,
    STOPWORDS_FILENAME,
    TERM_DOCUMENT_MATRIX_FILENAME
)

start = time.time()


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

 
    # get clean data for embeddings
    df1 = pd.read_csv(join(get_data_path(), INPUT_DATA_FILENAME), encoding="iso-8859-1")
     # preprocessing on both query and raw IATI description data
    clean_df = preprocess_embeddings(df1)
    query_df = preprocess_query_text(query)
    ##unpickling
    with open(join(get_data_path(), TERM_DOCUMENT_MATRIX_FILENAME), "rb") as _file:
                term_document_matrix = pickle.load(_file)
    
    with open(join(get_data_path(), VECTORIZER_FILENAME), "rb") as _file:
                vectorizer = pickle.load(_file)
    
    
    with open(join(get_data_path(), WORD_LIST_FILENAME), "rb") as _file:
                word_list = pickle.load(_file)
    
    with open(join(get_data_path(), IATI_IDENTIFIERS_FILENAME), "rb") as _file:
                iati_identifiers_list = pickle.load(_file)
                
                
#put tdm into df
xd = pd.DataFrame(term_document_matrix .toarray(), columns = vectorizer.get_feature_names())
xd.index = iati_identifiers_list
wordsintdm = list(xd.columns)
                
 
# get data ready into lists
def list_for_wordtovec(cdf,qdf):    
    f_vectorlist = [row['description'].split(" ") for index, row in cdf.iterrows()]
     #append query
    f_vectorlist.append(str(qdf['description']).split(" "))
    return f_vectorlist

vectorlist = list_for_wordtovec(clean_df,query_df)

#set up embeddings model
def getwordmodel(pdata, psize, pwindow, pmin):
    return Word2Vec(pdata, size= psize, window = pwindow, min_count = pmin)
    

#get word vectors
def getwordvectors(pmodel):
    return list(pmodel.wv.vocab)


###test of all functions
model = getwordmodel(vectorlist, 50, 5, 20)
##save embeddings model
model.wv.save_word2vec_format(MODEL_NAME)
#loaded_model = Word2Vec.load(MODEL_NAME)
words = getwordvectors(model)


# put embeddings into a df with words as rownames
def embeddings_in_df (pmodel, pwords):
         #empty df ready to populate
        f_dfvectors = pd.DataFrame(np.zeros((len(pwords),50)))
        #put embeddings into df
        for row in range(len(pwords)):
            f_dfvectors.loc[row] = np.array([list(pmodel.wv[pwords[row]])])
        #add in the words as rownames
        f_dfvectors.index = pwords
        return f_dfvectors


dfvectors = embeddings_in_df (model, getwordvectors(model))

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

r_qry = embeddings_for_qry(vectorlist, dfvectors, words)

qryvector= r_qry[0]
wordsinqry= r_qry[1]    


#for every vector in qryvector is compared to every value in word vectors
def cosine_res(pdfvector, pqryvector):
    f_similarwords={}   
    for index, value in enumerate(pqryvector):
        for index2, value2 in pdfvector.iterrows():
             cos_result = cosine_similarity(np.array(value).reshape(1, value.shape[0]), np.array(value2).reshape(1, value2.shape[0]))
             if cos_result > 0.9:
                     f_similarwords[index2] = round(float(cos_result),5)
    f_similarwords= sorted(f_similarwords.items(), key=operator.itemgetter(1), reverse=True)
    return f_similarwords

similarwords= cosine_res(dfvectors, qryvector)


def final_rank(psimilarwords, pwordsintdm):
    
    rankings = pd.Series()
    for wrds in psimilarwords:
        if wrds[0] in pwordsintdm:
             colData = xd[wrds[0]]
             colData=colData[colData!=0]
             rankings = rankings.append(colData)
    
    return(rankings.sort_values(ascending=False))         
 
print (final_rank(similarwords,wordsintdm ))

    
end = time.time()


print("completed in {0} seconds".format(end - start))
