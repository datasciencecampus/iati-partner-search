from unittest import TestCase
from ips_python.preprocessing import split_flatten_list

class TestPreprocessing(TestCase):
    def test_split_flatten_list(self):
        test_input = ['a b', 'c']
        expected_output = ['a', 'b', 'c']
        assert split_flatten_list(test_input) == expected_output
