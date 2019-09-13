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
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import wordnet
from langdetect import detect
import time

start = time.time()

#set wd to path to input files and where outputs will be written (leave blank if same directory as this script)
wd = r''

#To import full dataset
df1 = pd.read_csv(os.path.join(wd,'all_downloaded_records.csv'), encoding='iso-8859-1') 
df1 = df1[['iati.identifier','description','participating.org..Implementing.']]


#To import 10K
#data = pd.read_csv(os.path.join(wd,"test10k.csv"), encoding='iso-8859-1') 
#df1 = data[['iati-identifier','description','participating-org (Implementing)','reporting-org']]


def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
   
    return tag_dict.get(tag, wordnet.NOUN)


def preprocessing (p_df, p_text):
    
    #remove na description values
    p_df = p_df.dropna(subset=[p_text])
    
    #convert to string:
    p_df = p_df.astype(str)
                
    # remove punctuation
    p_df[p_text] = p_df[p_text].str.replace('[^\w\s]','')
    
    # remove underscores not picked up as punctuation above
    p_df[p_text] = p_df[p_text].str.replace('_','')
    
    # remove  numbers
    p_df[p_text] = p_df[p_text].str.replace('[\d+]','')

    # lowercase
    p_df[p_text] = p_df[p_text].apply(lambda x: " ".join(x.lower() for x in x.split()))
    
    # Remove empty string
    p_df = p_df[p_df[p_text]!='']
    
    #Remove entirely whitespace strings in description column
    p_df = p_df[~p_df[p_text].str.isspace()]
    
#    # only English language please
    for index, row in p_df.iterrows():
        try:
            if detect(row[p_text]) != 'en':
                p_df = p_df.drop(index)
        except:
            #get rid of any garbage
            p_df = p_df.drop(index)
   
    #remove stopwords English
    stop = stopwords.words('english')
    p_df[p_text] = p_df[p_text].apply(lambda x: " ".join(x for x in x.split() if x not in stop))

    #lemmatise text
    lemmatizer = WordNetLemmatizer() 
    p_df[p_text] = p_df[p_text].apply(lambda x:" ".join([lemmatizer.lemmatize(x, get_wordnet_pos(x)) for x in x.split()]))

    return (p_df)
 
df1= preprocessing(df1, 'description')

#write out df with reduced records
dfout = df1[['iati.identifier','description']]
dfout.to_csv(os.path.join(wd,'all_used_records.csv'))

#words occuring in only one document will not be included?  
min_proportion = 2*1/df1.shape[0]

#Build document-term matrix
vectorizer = TfidfVectorizer(min_df = min_proportion)
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