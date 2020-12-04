# -*- coding: utf-8 -*-
# Unit testing of tlhe naive_implementation.py file
from unittest import main, TestCase
import warnings
warnings.filterwarnings("ignore")
import argparse
import mmap
from parse import parse
from enum import Enum
import pandas as pd
from pandas.util.testing import assert_frame_equal
import sys
import os

class Constants(Enum):
    BASE_URL = '../main'
    expected_dir = '../expected_output'
    input_dir = '../input/'
    file1 = 'trip_data_sized1.txt'
    file2 = 'trip_data_sized2.txt'
    file3 = 'trip_data_sized4.txt'

# Importing the to be tested modules
sys.path.append(Constants.BASE_URL.value)
from naive_implementation import naive_implementation
from validate_results import validate_results

class Test(TestCase):
    def test_naive_implementation_file1(self):
        """
            Testing the implementation on file-1 (Size: 189372, Unique Drivers: 383)
        """
        # Extracting the output and associated expected file information
        to_be_tested = Constants.file1.value
        expected_output_path = os.path.join(Constants.expected_dir.value,
            to_be_tested)
        input_path = os.path.join(Constants.BASE_URL.value,
            Constants.input_dir.value, to_be_tested)
        current_output_path = naive_implementation(input_file=input_path)
        # Unit testing the module
        self.assertTrue(validate_results(expected_output_path, \
            current_output_path, 0)['status'][0])

    def test_naive_implementation_file2(self):
        """
            Testing the implementation on file-2 (Size: 8639, Unique Drivers: 131)
        """
        # Extracting the output and associated expected file information
        to_be_tested = Constants.file2.value
        expected_output_path = os.path.join(Constants.expected_dir.value,
            to_be_tested)
        input_path = os.path.join(Constants.BASE_URL.value,
            Constants.input_dir.value, to_be_tested)
        current_output_path = naive_implementation(input_file=input_path)
        # Unit testing the module
        self.assertTrue(validate_results(expected_output_path, \
            current_output_path, 0)['status'][0])

    def test_naive_implementation_file3(self):
        """
            Testing the implementation on file-3 (Size: 6, Unique Drivers: 3)
        """
        # Extracting the output and associated expected file information
        to_be_tested = Constants.file3.value
        expected_output_path = os.path.join(Constants.expected_dir.value,
            to_be_tested)
        input_path = os.path.join(Constants.BASE_URL.value,
            Constants.input_dir.value, to_be_tested)
        current_output_path = naive_implementation(input_file=input_path)
        # Unit testing the module
        self.assertTrue(validate_results(expected_output_path, \
            current_output_path, 0)['status'][0])

if __name__ == '__main__':
    main()
