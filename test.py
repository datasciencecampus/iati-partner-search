import pandas as pd
from preprocessing import preprocessing_language_detection, preprocessing_eng_only

COLUMN_NAME = 'description'

input_data_frame = pd.read_csv("test_input.csv")
expected_data_frame = pd.read_csv("test_output.csv")


def test_remove_na():
    assert COLUMN_NAME in list(expected_data_frame.columns)

    p_df = input_data_frame
    p_text = COLUMN_NAME

    p_df = p_df.dropna(subset=[p_text])
    # assert result[COLUMN_NAME][0] == 0

    p_df = p_df.astype(str)

    p_df[p_text] = p_df[p_text].str.replace('[^\w\s]','')

    p_df[p_text] = p_df[p_text].str.replace('_',' ')

    p_df[p_text] = p_df[p_text].str.replace('[\d+]','')

    p_df[p_text] = p_df[p_text].apply(lambda x: " ".join(x.lower() for x in x.split()))

    import nltk
    wordstokeep = set(nltk.corpus.words.words())
    p_df[p_text] = p_df[p_text].apply(lambda x:" ".join(x for x in x.split() if x in wordstokeep))

    result = p_df

    from pprint import pprint
    print("INPUT:")
    pprint(input_data_frame)
    print("RESULT:")
    pprint(result)
    print("EXPECTED:")
    pprint(expected_data_frame)

    assert expected_data_frame.equals(result)
