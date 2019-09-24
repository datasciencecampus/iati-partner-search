# -*- coding: utf-8 -*-
"""
IATI Partner Search 
1) Pre-process data 
2) Create term document matrix
3) Write term document matrix to Pickle file

"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import pickle
import os
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import time

start = time.time()

#set wd to path to input files and where outputs will be written (leave blank if same directory as this script)
wd = ''

#To import full dataset
df1 = pd.read_csv(os.path.join(wd,'all_downloaded_records.csv'), encoding='iso-8859-1') 
df1 = df1[['iati.identifier','description','participating.org..Implementing.']]

#To import 10K
#data = pd.read_csv(r"C:\Users\t-wilson\Documents\IATI_partner_search\test10k.csv") 
#df1 = data[['iati-identifier','description','participating-org (Implementing)','reporting-org']]

wordstokeep = set(nltk.corpus.words.words())

def preprocessing(p_df, p_text):
    
    #remove na description values
    p_df = p_df.dropna(subset=[p_text])
    
    #convert to string:
    p_df = p_df.astype(str)
                
    # remove punctuation
    p_df[p_text] = p_df[p_text].str.replace('[^\w\s]','')
    
    # remove underscores not picked up as punctuation above
    p_df[p_text] = p_df[p_text].str.replace('_',' ')
    
    # remove  numbers
    p_df[p_text] = p_df[p_text].str.replace('[\d+]','')

    # lowercase
    p_df[p_text] = p_df[p_text].apply(lambda x: " ".join(x.lower() for x in x.split()))
    
    #Remove word if not in English dictionary
    p_df[p_text] = p_df[p_text].apply(lambda x:" ".join(x for x in x.split() if x in wordstokeep))
    
    
    #Remove english stop words
    stop = stopwords.words('english')
    p_df[p_text] = p_df[p_text].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
    
    #Porter stemmer
    st = PorterStemmer()
    p_df[p_text] = p_df[p_text].apply(lambda x: " ".join([st.stem(word) for word in x.split()]))
    
    # Remove empty string
    p_df = p_df[p_df[p_text]!='']
    
    #Remove entirely whitespace strings in description column
    p_df = p_df[~p_df[p_text].str.isspace()]

    return (p_df)
  
df1= preprocessing(df1, 'description')

#write out df with reduced records
dfout = df1[['iati.identifier','description']]
dfout.to_csv(os.path.join(wd,'all_used_records_stemEngDict.csv'))

#words occuring in only one document will not be included?  
#min_proportion = 2*1/df1.shape[0]

#Build document-term matrix
vectorizer = TfidfVectorizer(min_df = 0) #replace with min_proportion variable if wish
X = vectorizer.fit_transform(df1['description'])

#write out the list of words to pickle file
word_list = vectorizer.get_feature_names()
outW = open(os.path.join(wd, 'wordList.pkl'), 'wb')
pickle.dump(word_list, outW)

#Write X to pickle file
out = open(os.path.join(wd, 'iatiFullTDM.pkl'), 'wb')
pickle.dump(X, out)
out.close()

end = time.time()

print("completed in {0} seconds".format(end - start))