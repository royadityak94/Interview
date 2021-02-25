#!/usr/bin/python3
# Adding src code to the test folder path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Loading the required packages
import unittest
from add_custom_words import add_new_words
from anagram_generator import get_anagrams
from character_tree import CharacterMap, create_charmap_dictionary
from unittest.mock import patch, Mock

# Helper module to unit test add_new_words(new_words)
class TestAddCustomWords(unittest.TestCase):
    '''Test Modules for add_custom_words.add_new_words
    '''

    @classmethod
    def setUpClass(self):
        pass

    @classmethod
    def tearDownClass(self):
        # Reverting the word dictionary to previous state
        create_charmap_dictionary()

    def test_default(self):
        new_words = ['berzuo', 'ozureb', 'eruzob', 'bourze']
        for idx, word in enumerate(new_words):
            self.assertEqual(get_anagrams(word), list())

        add_new_words(new_words)
        for idx, word in enumerate(new_words):
            with self.subTest(i=idx):
                expected = new_words[:]
                del expected[idx]
                self.assertEqual(get_anagrams(word), expected)

    def test_exception(self):
        new_words = ['berzuo', 'ozureb', 'eruzob', 'bourze']
        with self.assertRaises(Exception) as handler:
            with patch('utilities.persist_dictionary_file') as testMock:
                testMock.side_effect = Mock(side_effect=Exception())
                testMock()
                add_new_words(new_words)


if __name__ == '__main__':
    unittest.main()
