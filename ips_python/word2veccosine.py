import pandas as pd
from os.path import join
from gensim.models import Word2Vec
import pickle

try:
    from ips_python.utils import get_data_path
    from ips_python.preprocessing import preprocess_query_text
    from ips_python.cosine import get_cosine_similarity
    from ips_python.word2vecaverage import average_per_doc
    from ips_python.constants import (
        PROCESSED_RECORDS_FILENAME,
        COSINE_FILENAME,
        WORD2VECMODEL_FILENAME,
        WORD2VECAVG_FILENAME,
        DESCRIPTION_COLUMN_NAME,
    )
except ModuleNotFoundError:
    from utils import get_data_path
    from preprocessing import preprocess_query_text
    from cosine import get_cosine_similarity
    from word2vecaverage import average_per_doc
    from constants import (
        PROCESSED_RECORDS_FILENAME,
        COSINE_FILENAME,
        WORD2VECMODEL_FILENAME,
        WORD2VECAVG_FILENAME,
        DESCRIPTION_COLUMN_NAME,
    )


if __name__ == "__main__":

    query = """Despite impressive improvements in Vietnam's development and
        health status over the past decade, gains have not been equitable and significant unmet
        health needs remain. Poor and marginalized populations continue to disproportionally
        suffer from preventable illnesses while those in wealthier socioeconomic groups
        continue to enjoy greater health and longer life expectancy. Social Marketing for
        Improved Rural Health will include 3 main components: i) social marketing of SafeWat
        household water treatment solution and promotion of safer hygiene behaviors; ii) Good
        health, Great life and iii) behavior change communication to address non-supply side
        barriers to healthier behaviors."""

    model = Word2Vec.load(join(get_data_path(), WORD2VECMODEL_FILENAME))

    iati_records = pd.read_csv(
        join(get_data_path(), PROCESSED_RECORDS_FILENAME), encoding="utf-8"
    )

    query_df = preprocess_query_text(query)

    if not query_df.empty:

        with open(join(get_data_path(), WORD2VECAVG_FILENAME), "rb") as _file:
            full_arr = pickle.load(_file)

        query_average = average_per_doc(
            str(query_df[DESCRIPTION_COLUMN_NAME]), model, 300
        ).reshape(1, -1)

        # Using get_cosine_similarity from our cosine.py script, it removes cosine < 0 results
        out_df = get_cosine_similarity(query_average, full_arr, iati_records)

        out_df.to_csv(
            join(get_data_path(), COSINE_FILENAME), index=False, encoding="utf-8"
        )
