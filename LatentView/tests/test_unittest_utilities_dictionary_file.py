#!/usr/bin/python3
# Adding src code to the test folder path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Loading the required packages
import unittest
from utilities import fetch_dictionary_file, is_non_zero_file, fetch_dictionary_information, persist_dictionary_file
from character_tree import CharacterMap
from unittest.mock import patch, mock_open

# Helper module to unit test fetch_dictionary_file(dict_file_path)
class TestFetchDictionaryFile(unittest.TestCase):
    '''Test Modules for utilities.fetch_dictionary_file
    '''

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

# Helper module to unit test persist_dictionary_file(character_dictionary, dict_file_path)
class TestPersistDictionaryFile(unittest.TestCase):
    '''Test Modules for utilities.persist_dictionary_file
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

    def get_character_dictionary(self, data):
        character_dictionary = dict()
        for word in data:
            chars = word.lower()
            character_dictionary.update({chars: CharacterMap(chars)})
        return character_dictionary

    def assertMapEquality(self, map1, map2):
        for key in map1:
            if key not in map2 or map1[key].mapper != map2[key].mapper:
                return False
        return True

    def test_default(self):
        data = self.split_contents('alpha\nbeta\ngamma'.encode('utf-8'))
        character_dictionary = self.get_character_dictionary(data)
        persist_dictionary_file(character_dictionary, self.dict_file_path)
        actual = fetch_dictionary_file(self.dict_file_path)
        self.assertTrue(self.assertMapEquality(actual, character_dictionary))

    def test_single_element(self):
        data = self.split_contents('alpha\n'.encode('utf-8'))
        character_dictionary = self.get_character_dictionary(data)
        persist_dictionary_file(character_dictionary, self.dict_file_path)
        actual = fetch_dictionary_file(self.dict_file_path)
        self.assertTrue(self.assertMapEquality(actual, character_dictionary))

    def test_empty(self):
        data = self.split_contents(''.encode('utf-8'))
        character_dictionary = self.get_character_dictionary(data)
        persist_dictionary_file(character_dictionary, self.dict_file_path)
        actual = fetch_dictionary_file(self.dict_file_path)
        self.assertTrue(self.assertMapEquality(actual, character_dictionary))


# Helper module to unit test fetch_dictionary_information(properties=None, group = None)
class TestFetchDictionaryInformation(unittest.TestCase):
    '''Test Modules for utilities.fetch_dictionary_information
    '''

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
