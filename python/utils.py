from datetime import datetime

def get_timestamp_string_prefix():
    """
    return the date and time as a string in the format 2019_10_14_18_14_11
    """
    return datetime.now().strftime("%G_%m_%d_%H_%M_%S")
