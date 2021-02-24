#!/usr/bin/python3
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
from utilities import fetch_dictionary_file, is_non_zero_file, fetch_dictionary_information
from character_tree import CharacterMap
from unittest.mock import patch, mock_open

# Helper module to unit test fetch_dictionary_file(dict_file_path)
class TestFetchDictionaryFile(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        pass
        
    @classmethod
    def tearDownClass(self):
        pass
        
    def test_default(self):
        self.assertTrue(len(fetch_dictionary_file('../working/shelve_dict.pickle')) > 0)
    
    def test_incorrect_file_path(self):
        with self.assertRaises(AssertionError) as context:
            fetch_dictionary_file('working/shelve_dict.pickle')
        self.assertTrue('Empty file, please proceed to load the dictionary first' in str(context.exception))

# Helper module to unit test fetch_dictionary_information(properties=None, group = None)
class TestFetchDictionaryInformation(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        pass
        
    @classmethod
    def tearDownClass(self):
        pass
        
    def test_default(self):
        self.assertTrue(is_non_zero_file(fetch_dictionary_information()))
    

if __name__ == '__main__':
    unittest.main()