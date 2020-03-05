import time
from os.path import join

import pandas as pd

try:
    from ips_python.utils import get_data_path
    from ips_python.constants import (
        INPUT_DATA_FILENAME,
        COSINE_FILENAME,
        IATI_IDENTIFIER_COLUMN_NAME,
        TITLE_COLUMN_NAME,
        DESCRIPTION_COLUMN_NAME,
        ORG_ID_COLUMN_NAME,
        IATI_FIELDS,
    )
    from ips_python.preprocessing import preprocessing_initial_text_clean
except ModuleNotFoundError:
    from utils import get_data_path
    from constants import (
        INPUT_DATA_FILENAME,
        COSINE_FILENAME,
        IATI_IDENTIFIER_COLUMN_NAME,
        TITLE_COLUMN_NAME,
        DESCRIPTION_COLUMN_NAME,
        ORG_ID_COLUMN_NAME,
        IATI_FIELDS,
    )
    from preprocessing import preprocessing_initial_text_clean


def process_results(initial_result_df, full_iati_records, number_of_results=100):
    """
    This is an example of Google style.

    Args:
        param1: This is the first param.
        param2: This is a second param.

    Returns:
        This is a description of what is returned.

    Raises:
        KeyError: Raises an exception.
    """
    start_time = time.time()
    keep_columns = IATI_FIELDS
    full_iati_df = full_iati_records[keep_columns]
    print("select columns after {} seconds".format(time.time() - start_time))

    # Select unique record on all fields but iati.identifier, include iati.identifer of 1st record in duplicate set (!!!)
    make_unique = [f for f in keep_columns if f != IATI_IDENTIFIER_COLUMN_NAME]
    full_iati_df.drop_duplicates(subset=make_unique, keep="first")
    print("duplicates dropped after {} seconds".format(time.time() - start_time))

    full_iati_df = full_iati_df.merge(
        initial_result_df, on=IATI_IDENTIFIER_COLUMN_NAME, how="inner"
    )
    print("joined cosine res after {} seconds".format(time.time() - start_time))

    full_iati_df.sort_values(by="cosine_sim", ascending=False, inplace=True)
    print("sorted by res after {} seconds".format(time.time() - start_time))

    full_iati_df = full_iati_df.head(number_of_results)
    print("limited after {} seconds".format(time.time() - start_time))

    """further filtering ideas remove results with null description e.g. matched on title alone"""

    return full_iati_df


def remove_white_space(refined_res, p_text):

    # remove extra spaces and spaces at the end of string from reporting.org column

    refined_res[p_text] = (refined_res[p_text].str.split()).str.join(" ")

    refined_res[p_text] = refined_res[p_text].str.rstrip()

    return refined_res


def gather_top_results(post_processed_results, org_name, number_of_results_per_org):

    start_time = time.time()
    # remove duplicate entries
    post_processed_results.drop_duplicates(
        subset=[org_name, TITLE_COLUMN_NAME, DESCRIPTION_COLUMN_NAME]
    )

    # set order for top reporting organisations
    myorder = pd.Series(post_processed_results[org_name], name="A").unique()
    sorterIndex = dict(zip(myorder, range(len(myorder))))

    post_processed_results["myorder"] = post_processed_results[org_name].map(
        sorterIndex
    )

    # group entries by reporting.org, taking top entries
    top_project_results = post_processed_results.groupby("myorder").head(
        number_of_results_per_org
    )

    # Order by top organisation and within each top organisation the top projects
    top_project_results = top_project_results.sort_values(
        ["myorder", "cosine_sim"], ascending=[True, False]
    )

    top_project_results = top_project_results.drop(["myorder"], axis=1)

    print("limited after {} seconds".format(time.time() - start_time))

    return top_project_results


if __name__ == "__main__":

    full_df = pd.read_csv(join(get_data_path(), INPUT_DATA_FILENAME), encoding="utf-8")

    cosine_res_df = pd.read_csv(
        join(get_data_path(), COSINE_FILENAME), encoding="utf-8"
    )

    refined_res = process_results(cosine_res_df, full_df, 100)

    refined_res = preprocessing_initial_text_clean(refined_res, ORG_ID_COLUMN_NAME)

    refined_res = remove_white_space(refined_res, ORG_ID_COLUMN_NAME)
    refined_res = remove_white_space(refined_res, DESCRIPTION_COLUMN_NAME)

    # top results per reporting organisation
    top_project_results = gather_top_results(refined_res, ORG_ID_COLUMN_NAME, 3)
