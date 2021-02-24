#!/usr/bin/python3
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
from utilities import load_data_from_file
from unittest.mock import patch, mock_open

class FileWriter:
    @staticmethod
    def write(file_path, content):
        with open(file_path, 'wb') as file:
            print ("Wrote: ", content)
            file.write(content)

# Helper module to unit test load_data_from_file(file_path)
class TestFormattedStrings(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.mocked_path = 'new_words.txt'
        
    @classmethod
    def tearDownClass(self):
        del self.mocked_path
    
    def split_contents(self, content):
        if not content:
            return frozenset()
        return frozenset(content.decode('utf-8').split('\n'))
        
    def test_default(self):
        mocked_contents = 'alpha\nbeta\ngamma\nzetaa\nkappa'.encode('utf-8')
        expected = self.split_contents(mocked_contents)
        actual = None
        with patch('mmap.mmap', mock_open(read_data=mocked_contents)) as mocked_file:
            actual = load_data_from_file(self.mocked_path)
        self.assertEqual(actual, expected)
    
    def test_empty_file(self): 
        mocked_contents = ''.encode('utf-8')
        expected = self.split_contents(mocked_contents)
        actual = None
        with patch('mmap.mmap', mock_open(read_data=mocked_contents)) as mocked_file:
            actual = load_data_from_file(self.mocked_path)
        self.assertEqual(actual, expected)
    
    def test_single_content(self): 
        mocked_contents = 'all'.encode('utf-8')
        expected = self.split_contents(mocked_contents)
        actual = None
        with patch('mmap.mmap', mock_open(read_data=mocked_contents)) as mocked_file:
            actual = load_data_from_file(self.mocked_path)
        self.assertEqual(actual, expected)
            
if __name__ == '__main__':
    unittest.main()