#Authors: Saliha MInhas,  Date: 29th September 2019

# this version was improved upon by Tom Wilson
# and subsequently the lemmatisers/lang detect were removed
# and stemmer and nltk dictionry to zap all non English words reinstated

#Description
# preprocessing  with lemmatisers/pos tagger and lang detect

import numpy as np
import pandas as pd
import nltk
import time
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import WordNetLemmatizer 
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import wordnet
from langdetect import detect


start = time.time()

data = pd.read_csv("C:/corpus3/test10k.csv",  encoding="ANSI") 
df1 = pd.DataFrame(data[['title','description']])

def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
   
    return tag_dict.get(tag, wordnet.NOUN)

def preprocessing (p_df, p_text):

    # only English language please
    for index, row in p_df.iterrows():
         row[p_text] = str(row[p_text])
         if str(row[p_text]) != " " and len (row[p_text])> 2:
            if detect(row[p_text]) != 'en':
                   p_df.drop(index, inplace=True)
            
    
    # remove punctuation
    p_df[p_text] = p_df[p_text].str.replace('[^\w\s]','')

    # remove  numbers
    p_df[p_text] = p_df[p_text].str.replace('[\d+]','')

    # lowercase
    p_df[p_text] = p_df[p_text].apply(lambda x: " ".join(x.lower() for x in x.split()))
 
   
    #remove stopwords English
    stop = stopwords.words('english')
    p_df[p_text] = p_df[p_text].apply(lambda x: " ".join(x for x in x.split() if x not in stop))

    #lemmatise text
    lemmatizer = WordNetLemmatizer() 
    p_df[p_text] = p_df[p_text].apply(lambda x:" ".join([lemmatizer.lemmatize(x, get_wordnet_pos(x)) for x in x.split()]))

    return (p_df)
 
pd.df1 = preprocessing(df1, 'description')
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df1['description'])

#if want to look at it
xd = pd.DataFrame(X.toarray(), columns = vectorizer.get_feature_names())



print (time.time()- start)




















