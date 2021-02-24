#!/usr/bin/python3
import sys
import os
import shutil
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
from utilities import create_dictionary, fetch_dictionary_file
from unittest.mock import patch, mock_open
from character_tree import CharacterMap

class FileWriter:
    @staticmethod
    def write(file_path, content):
        with open(file_path, 'wb') as file:
            print ("Wrote: ", content)
            file.write(content)

# Helper module to unit test create_dictionary(data, dict_file_path, CharacterMap)
class TestCreateDictionary(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.dict_file_path = os.path.join('test', 'test_dict.pickle')
        
    @classmethod
    def tearDownClass(self):
        dict_file_dir = dict_file_path[:len(dict_file_path) - dict_file_path[::-1].find('/')]
        shutil.rmtree(self.dict_file_path) 
        del self.dict_file_path
    
    def split_contents(self, content):
        if not content:
            return frozenset()
        return frozenset(content.decode('utf-8').split('\n'))
        
    def test_default(self):
        data = self.split_contents('alpha\nbeta\ngamma'.encode('utf-8'))
        
        expected = {word: CharacterMap(word) for word in data}
        create_dictionary(data, self.dict_file_path, CharacterMap)
        actual = fetch_dictionary_file(self.dict_file_path)
        self.assertEqual(actual, expected)
    

            
if __name__ == '__main__':
    unittest.main()