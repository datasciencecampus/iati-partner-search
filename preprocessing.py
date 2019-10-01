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

def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)


def preprocessing_language_detection(p_df, p_text):

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


def preprocessing_eng_only(p_df, p_text):
    wordstokeep = set(nltk.corpus.words.words())

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
