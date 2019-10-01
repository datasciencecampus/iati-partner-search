# -*- coding: utf-8 -*-
"""
IATI Partner Search 
1) Pre-process data - check word is in Eng Dict, then stem
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
df1 = df1[['iati.identifier','description','title']]

#Remove empty string iati identifiers
df1 = df1[df1['iati.identifier']!= '']
df1 = df1[~df1['iati.identifier'].str.isspace()]
df1 = df1.reset_index(drop=True)

#If both description and title not NA concatenate them into description column
df1.loc[~df1['description'].isna() & ~df1['title'].isna(), ['description']] =df1['title'] +" "+df1['description'] 

#If description is NA replace with title
df1.loc[df1['description'].isna(), ['description']]=df1['title']

#To import 10K
#data = pd.read_csv(r"C:\Users\t-wilson\Documents\IATI_partner_search\test10k.csv") 
#df1 = data[['iati-identifier','description','participating-org (Implementing)','reporting-org']]

wordstokeep = set(nltk.corpus.words.words())

def append_to_stop(stoplist, inputfile):
    with open(inputfile, 'r') as r:
        new_words = r.read().splitlines()
    return stoplist + new_words

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
    #add custom stop words
    stop = append_to_stop(stop, os.path.join(wd, 'stopwords.txt'))
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
with open(os.path.join(wd, 'wordListstemEngDict.pkl'), 'wb') as outW:
    pickle.dump(word_list, outW)

#Write X to pickle file
with open(os.path.join(wd, 'iatiFullTDMstemEngDict.pkl'), 'wb') as out:
    pickle.dump(X, out)
    
#Write out the IDF array to pickle file (one IDF value per unique word)
with open(os.path.join(wd, 'iatiTDM_IDFstemEngDict.pkl'), 'wb') as out:
    pickle.dump(vectorizer.idf_, out)

end = time.time()

print("completed in {0} seconds".format(end - start))