from preprocessing import preprocessing_language_detection, preprocessing_eng_only

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

