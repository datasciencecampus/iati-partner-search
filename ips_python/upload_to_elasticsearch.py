import requests
import pandas as pd
from os import getenv
from os.path import join, dirname
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from dotenv import load_dotenv
from urllib.parse import urljoin

try:
    from ips_python.utils import get_raw_data_filepath
    from ips_python.constants import ELASTICSEARCH_INDEX_NAME
except ModuleNotFoundError:
    from utils import get_raw_data_filepath
    from constants import ELASTICSEARCH_INDEX_NAME


def ensure_elasticsearch_keeps_malformed_fields(elasticsearch_url, elasticsearch_index_name):
    elasticsearch_index_url = urljoin(elasticsearch_url, elasticsearch_index_name)
    HEADERS = {"Content-Type": "application/json"}
    data = '{"settings": {"index.mapping.ignore_malformed": true}}'
    res = requests.put(elasticsearch_index_url, headers=HEADERS, data=data, verify=False)


def document_generator(dataframe, elasticsearch_index_name):
    """
    generate the chunked documents for upload to elasticsearch

    Args:
        param1: A Pandas dataframe
        param2: The name of the index on elasticsearch
    """
    dataframe_without_nan = dataframe.fillna('')
    dataframe_iterator = dataframe_without_nan.iterrows()

    for index, document in dataframe_iterator:
        yield {"_index": elasticsearch_index_name, "_type": "_doc", "_id": f"{document['id']}", **document}


def main(elasticsearch_url):
    print("Setting up cluster config")
    elasticsearch_instance = Elasticsearch([elasticsearch_url], timeout=30)

    print("Allowing malformed data")
    ensure_elasticsearch_keeps_malformed_fields(elasticsearch_url, ELASTICSEARCH_INDEX_NAME)

    print("Reading dataframe")
    processed_iati_records = pd.read_csv(get_raw_data_filepath(), encoding="iso-8859-1")

    print("Uploading data")
    helpers.bulk(elasticsearch_instance, document_generator(processed_iati_records, ELASTICSEARCH_INDEX_NAME))


def delete_elasticsearch_index(elasticsearch_url, elasticsearch_index_name):
    print("Setting up cluster config")
    elasticsearch_instance = Elasticsearch([elasticsearch_url])

    print("Deleting index")
    elasticsearch_instance.indices.delete(index=elasticsearch_index_name)


if __name__ == "__main__":
    dotenv_path = join(dirname(dirname(__file__)), ".env")
    load_dotenv(dotenv_path)

    elasticsearch_url = getenv("ELASTICSEARCH_URL")

    main(elasticsearch_url)
