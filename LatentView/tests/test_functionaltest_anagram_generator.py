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

# Helper module to unit test get_anagrams(input_string, maximum_size=None)
class TestEndToEndModuleForAnagramGenerator(unittest.TestCase):
    '''Test Modules for anagram_generator.get_anagrams
    '''

    @classmethod
    def setUpClass(self):
        pass

    @classmethod
    def tearDownClass(self):
        pass

    def test_defaults(self):
        words_testable = {'loop': ['polo', 'pool'], 'loops': ['polos', 'sloop', 'spool'],
            'aeprs': ['asper', 'spear', 'prase', 'parse', 'spare', 'spaer'], 'blitzkrig': []}

        for word, resultant in words_testable.items():
            got = get_anagrams(word)
            with self.subTest(word=word, resultant=resultant, type='Mismatch in contents'):
                self.assertEqual(sorted(got), sorted(resultant))

            with self.subTest(word=word, resultant=resultant, type='Mismatch in length'):
                self.assertEqual(len(got), len(resultant))

    def test_all_present(self):
        words_testable = {'loop': ['polo', 'pool'], 'loops': ['polos', 'sloop', 'spool'],
            'aeprs': ['asper', 'spear', 'prase', 'parse', 'spare', 'spaer']}

        for word, resultant in words_testable.items():
            got = get_anagrams(word)
            with self.subTest(word=word, resultant=resultant, type='Mismatch in contents'):
                self.assertEqual(sorted(got), sorted(resultant))

            with self.subTest(word=word, resultant=resultant, type='Mismatch in length'):
                self.assertEqual(len(got), len(resultant))

    def test_all_new(self):
        words_testable = {'blitzkrig': [], 'blitzsdxsskrig': [], 'werawqpmaezig': []}

        for word, resultant in words_testable.items():
            got = get_anagrams(word)
            with self.subTest(word=word, resultant=resultant, type='Mismatch in contents'):
                self.assertEqual(sorted(got), sorted(resultant))

            with self.subTest(word=word, resultant=resultant, type='Mismatch in length'):
                self.assertEqual(len(got), len(resultant))

if __name__ == '__main__':
    unittest.main()
