from utils import get_timestamp_string_prefix

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import pickle
import os
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import time


def preprocess_example(file_path_to_data):
    """preprocessing function.

    Args:
        file_path_to_data: The first parameter.

    Returns:
        A list of strings that have been processed

    """
    print("I am doing something")
    
    return None


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

if __name__ == "__main__":

    start = time.time()

    #set working_directory to path to input files and where outputs will be written (leave blank if same directory as this script)
    working_directory = ''

    INPUT_DATA_DIRECTORY = "data"
    INPUT_DATA_FILENAME = 'all_downloaded_records.csv'

    INTERIM_DATA_DIRECTORY = 'interim_data'
    INTERIM_DATA_WORD_LIST = 'wordList.pkl'
    INTERIM_DATA_TERM_DOCUMENT_MATRIX = 'iatiFullTDM.pkl'
    INTERIM_DATA_USED_RECORDS = 'all_used_records_stemEngDict.csv'

    #To import full dataset
    df1 = pd.read_csv(os.path.join(working_directory, INPUT_DATA_DIRECTORY, INPUT_DATA_FILENAME), encoding='iso-8859-1')
    df1 = df1[['iati.identifier','description','participating.org..Implementing.']]

    #To import 10K
    #data = pd.read_csv(r"C:\Users\t-wilson\Documents\IATI_partner_search\test10k.csv")
    #df1 = data[['iati-identifier','description','participating-org (Implementing)','reporting-org']]

    df1= preprocessing_eng_only(df1, 'description')

    #write out df with reduced records
    dfout = df1[['iati.identifier','description']]
    dfout.to_csv(os.path.join(working_directory, INTERIM_DATA_DIRECTORY, INTERIM_DATA_USED_RECORDS))

    #words occuring in only one document will not be included?
    #min_proportion = 2*1/df1.shape[0]

    #Build document-term matrix
    vectorizer = TfidfVectorizer(min_df = 0) #replace with min_proportion variable if wish
    X = vectorizer.fit_transform(df1['description'])

    #write out the list of words to pickle file
    word_list = vectorizer.get_feature_names()
    with open(os.path.join(working_directory, INPUT_DATA_DIRECTORY, INTERIM_DATA_WORD_LIST), 'wb') as output_file:
        pickle.dump(word_list, output_file)

    #Write X to pickle file
    with open(os.path.join(working_directory, INPUT_DATA_DIRECTORY, INTERIM_DATA_TERM_DOCUMENT_MATRIX), 'wb') as output_file:
        pickle.dump(X, output_file)

    end = time.time()

    print("completed in {0} seconds".format(end - start))
