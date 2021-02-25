#!/usr/bin/python3
# Adding src code to the test folder path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Loading the required packages
import unittest
from utilities import create_dictionary, fetch_dictionary_file
from unittest.mock import patch, mock_open
from character_tree import CharacterMap


# Helper module to unit test create_dictionary(data, dict_file_path, CharacterMap)
class TestCreateDictionary(unittest.TestCase):
    '''Test Modules for utilities.create_dictionary
    '''

    @classmethod
    def setUpClass(self):
        self.dict_file_path = os.path.join('test', 'test_dict.pickle')

    @classmethod
    def tearDownClass(self):
        dict_file_dir = self.dict_file_path[:len(self.dict_file_path) - self.dict_file_path[::-1].find('/')]
        os.remove(self.dict_file_path)
        os.rmdir(dict_file_dir)
        del self.dict_file_path

    def split_contents(self, content):
        if not content:
            return frozenset()
        return frozenset(content.decode('utf-8').split('\n'))

    def test_default(self):
        data = self.split_contents('alpha\nbeta\ngamma'.encode('utf-8'))
        create_dictionary(data, self.dict_file_path, CharacterMap)
        actual = frozenset(fetch_dictionary_file(self.dict_file_path).keys())
        self.assertEqual(data, actual)

    def test_empty(self):
        data = self.split_contents(''.encode('utf-8'))
        create_dictionary(data, self.dict_file_path, CharacterMap)
        actual = frozenset(fetch_dictionary_file(self.dict_file_path).keys())
        self.assertEqual(data, actual)


if __name__ == '__main__':
    unittest.main()
