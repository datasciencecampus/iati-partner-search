# -*- coding: utf-8 -*-
"""
1) Take the mean tf-idf per word stored in the document-term matrix calculated by sklearn
2) Add this mean to the word list and write to csv
"""

import pandas as pd
import numpy as np
import os
import pickle

wd = r'C:\Users\t-wilson\Documents\IATI_partner_search\download_stemEngDict'

#Import iati.identifier csv for records included in doc-term matrix


#Import Pickle file (need both IATI dataframe and term document matrix to be read in for this script)
with open(os.path.join(wd,'iatiFullTDMstemEngDict.pkl'), "rb") as f:
    X = pickle.load(f)

#Calculate average tf-idf per word WHERE > 0 (as calculated by tfidfvectorizer)
avTFIDF = np.array(X.sum(axis=0)).flatten()/ X.getnnz(axis=0)

#Add average tf-idf to word list
words = pd.read_csv(os.path.join(wd, 'wordsListStemEngDict.csv'), encoding='iso-8859-1')
words['av_tfidf'] = avTFIDF

#Get the words greater than 0
nonZeroCount = X.getnnz(axis=0)

words['count'] = nonZeroCount

#write to csv
words.to_csv(os.path.join(wd, 'wordsbyAvTFIDFCount.csv'), index = False)

