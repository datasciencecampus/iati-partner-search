from constants import INPUT_DATA_FILENAME, COSINE_FILENAME
from os.path import join
from utils import get_data_path
import pandas as pd
import time


def process_results(initial_result_df, full_iati_records, number_of_results=100):

    start_time = time.time()
    keep_columns = [
        "iati.identifier",
        "reporting.org",
        "participating.org..Implementing.",
        "title",
        "description",
        "start.actual",
        "recipient.country",
        "total.Expenditure"
    ]
    full_iati_df = full_iati_records[keep_columns]
    print("select columns after {} seconds".format(time.time() - start_time))

    # Select unique record on all fields but iati.identifier, include iati.identifer of 1st record in duplicate set (!!!)
    make_unique = [f for f in keep_columns if f != "iati.identifier"]
    full_iati_df.drop_duplicates(subset=make_unique, keep="first")
    print("duplicates dropped after {} seconds".format(time.time() - start_time))

    full_iati_df = full_iati_df.merge(
        initial_result_df, on="iati.identifier", how="inner"
    )
    print("joined cosine res after {} seconds".format(time.time() - start_time))

    full_iati_df.sort_values(by="cosine_sim", ascending=False, inplace=True)
    print("sorted by res after {} seconds".format(time.time() - start_time))

    full_iati_df = full_iati_df.head(number_of_results)
    print("limited after {} seconds".format(time.time() - start_time))

    """further filtering ideas remove results with null description e.g. matched on title alone"""

    return full_iati_df


if __name__ == "__main__":

    full_df = pd.read_csv(
        join(get_data_path(), INPUT_DATA_FILENAME), encoding="iso-8859-1"
    )

    cosine_res_df = pd.read_csv(
        join(get_data_path(), COSINE_FILENAME), encoding="iso-8859-1"
    )

    refined_res = process_results(cosine_res_df, full_df, 100)


# getting the top 3 results for unique reporting.org
    
    #preprocess the reporting organisations
    
    

    # remove duplicate entries
    refined_res_no_duplicates = refined_res.drop_duplicates(subset = ["reporting.org", "title", "description"])
    
    # set order for top reporting organisations
    myorder = pd.Series(refined_res_no_duplicates["reporting.org"], name = 'A').unique()  
    sorterIndex = dict(zip(myorder, range(len(myorder))))
    
    refined_res_no_duplicates['myorder'] = refined_res_no_duplicates['reporting.org'].map(sorterIndex)
    
    # group entries by reporting.org, taking top three entries
    refined_res_grouped = refined_res_no_duplicates.groupby('myorder').head(2)
    
    # group                     
    refined_res_grouped = refined_res_grouped.sort_values(['myorder', 'cosine_sim'], ascending = [True, False])
    refined_res_grouped.get_group('AidData')
    
    refined_res_no_duplicates = refined_res.drop_duplicates(subset = ["reporting.org"])
    # "title", "description"
# column names in the provisional larger IATI dataset

"""
iati.identifier
hierarchy
last.updated.datetime
default.language
reporting.org
reporting.org.ref
reporting.org.type
reporting.org.type.code
title
description
activity.status.code
start.planned
end.planned
start.actual
end.actual
participating.org..Accountable.
participating.org.ref..Accountable.
participating.org.type..Accountable.
participating.org.type.code..Accountable.
participating.org..Funding.
participating.org.ref..Funding.
participating.org.type..Funding.
participating.org.type.code..Funding.
participating.org..Extending.
participating.org.ref..Extending.
participating.org.type..Extending.
participating.org.type.code..Extending.
participating.org..Implementing.
participating.org.ref..Implementing.
participating.org.type..Implementing.
participating.org.type.code..Implementing.
recipient.country.code
recipient.country
recipient.country.percentage
recipient.region.code
recipient.region
recipient.region.percentage
sector.code
sector
sector.percentage
sector.vocabulary
sector.vocabulary.code
collaboration.type.code
default.finance.type.code
default.flow.type.code
default.aid.type.code
default.tied.status.code
default.currency
currency
total.Commitment
total.Disbursement
total.Expenditure
total.Incoming.Funds
total.Interest.Repayment
total.Loan.Repayment
total.Reimbursement
cosine_sim
"""
