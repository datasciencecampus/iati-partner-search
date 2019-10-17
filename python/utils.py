from os.path import join, dirname, abspath
from datetime import datetime

def get_timestamp_string_prefix():
    """
    return the date and time as a string in the format 2019_10_14_18_14_11
    """
    return datetime.now().strftime("%G_%m_%d_%H_%M_%S")

def get_data_path():
    """
    Return the absolute filepath of the data directory

    Should work consistently across OS
    """
    return join(dirname(dirname(abspath(__file__))), "data")

def get_input_path():
    """
    Return the absolute filepath of the data directory

    Should work consistently across OS
    """
    return join(dirname(dirname(abspath(__file__))), "input")
