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

# Helper module to unit test get_anagrams(input_string, maximum_size=None)
class TestGetAnagrams(unittest.TestCase):
    '''Test Modules for anagram_generator.get_anagrams
    '''

    @classmethod
    def setUpClass(self):
        pass

    @classmethod
    def tearDownClass(self):
        pass

    def test_fetch_anagrams_loop(self):
        expected = ['polo', 'pool']
        got = sorted(get_anagrams('loop'))
        self.assertEqual(expected, got)

    def test_fetch_anagrams_loop_with_limit(self):
        expected = ['polo', 'pool']
        got = get_anagrams('loop', 1)
        for anagram in got:
            self.assertTrue(anagram in expected)

    def test_fetch_anagrams_loops(self):
        expected = ['polos', 'sloop', 'spool']
        got = sorted(get_anagrams('loops'))
        self.assertEqual(expected, got)

    def test_fetch_anagrams_loops_with_limit(self):
        expected = ['polos', 'sloop', 'spool']
        got = sorted(get_anagrams('loops', 2))
        for anagram in got:
            self.assertTrue(anagram in expected)

    def test_fetch_anagram_aeprs(self):
        expected = sorted(['asper', 'spear', 'prase', 'parse', 'spare', 'spaer'])
        got = sorted(get_anagrams('aeprs'))
        self.assertTrue(expected == got)

    def test_fetch_anagram_aeprs_length(self):
        got = sorted(get_anagrams('aeprs'))
        self.assertTrue(len(got) == 6)

    def test_fetch_empty_anagram(self):
        expected = []
        got = sorted(get_anagrams('blitzkrig'))
        self.assertEqual(expected, got)

    def test_exception(self):
        with self.assertRaises(Exception) as handler:
            with patch('CharacterMap') as testMock:
                testMock.side_effect = Mock(side_effect=Exception())
                testMock()
                get_anagrams('listen', 1)

if __name__ == '__main__':
    unittest.main()
