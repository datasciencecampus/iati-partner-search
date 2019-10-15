from utils import get_timestamp_string_prefix, get_data_path
from preprocessing import preprocessing_eng_only
from vectorize import vectorize


def download_data():
    """
    this is a placeholder function to show that we need to run something in order to procure the data
    """
    pass


def main():
    download_data()
    preprocessing_eng_only()
    vectorize()


def process_query(query_text):
    pass


if __name__ == "__main__":
    main()