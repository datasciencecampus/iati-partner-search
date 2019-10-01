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


#Import Pickle file of doc-term matrix
with open(os.path.join(wd,'iatiFullTDMstemEngDict.pkl'), "rb") as f:
    X = pickle.load(f)

#Import Pickle file of IDF
with open(os.path.join(wd, 'iatiTDM_IDFstemEngDict.pkl'), 'rb') as f:
    idf = pickle.load(f)
    
#Import Pickle file of word list
with open(os.path.join(wd, 'wordListstemEngDict.pkl'), 'rb') as f:
    words = pickle.load(f)
    
wordsDF = pd.DataFrame(words, columns=['word'])

#Add average idf to word list
wordsDF['idf'] = idf

#Get the words greater than 0
nonZeroCount = X.getnnz(axis=0)

wordsDF['count'] = nonZeroCount

#write to csv
wordsDF.to_csv(os.path.join(wd, 'StemmingWordsFreqIDF.csv'), index = False)

