#!/usr/bin/python3
# Adding src code to the test folder path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Loading the required packages
import unittest
from anagram_class_coroutines import AnagramGenerator
from character_tree import CharacterMap

# Helper module to unit test AnagramGenerator().get_anagrams(self, string, maximum_size=None)
class TestEndToEndModuleForAnagramGenerator(unittest.TestCase):
    '''Test Modules for anagram_generator.get_anagrams
    '''

    @classmethod
    def setUpClass(self):
        self.instance = AnagramGenerator()

    @classmethod
    def tearDownClass(self):
        del self.instance

    def test_defaults(self):
        words_testable = {'loop': True, 'polo': True, 'listen': True, 'silent': True,
            'arteezmis': False, 'misrateez': False, 'maeseztri': False, 'amseeztir': False}
        missing_words = []
        for word, is_present in words_testable.items():
            with self.subTest(word=word, is_present=is_present, type='Before Adding Custom Words'):
                got = self.instance.get_anagrams(word)
                if is_present:
                    self.assertTrue(len(got) > 0)
                else:
                    self.assertEqual(len(got), 0)
                    missing_words += word,

        self.instance.add_custom_words(missing_words)
        for word in missing_words:
            with self.subTest(word=word, is_present=True, type='After Adding Custom Words'):
                got = self.instance.get_anagrams(word)
                self.assertTrue(len(got) > 0)

    def test_all_present(self):
        self.instance = AnagramGenerator()
        words_testable = {'loop': True, 'polo': True, 'listen': True, 'silent': True}
        missing_words = []
        for word, is_present in words_testable.items():
            with self.subTest(word=word, is_present=is_present, type='Before Adding Custom Words'):
                got = self.instance.get_anagrams(word)
                if is_present:
                    self.assertTrue(len(got) > 0)
                else:
                    self.assertEqual(len(got), 0)
                    missing_words += word,

        self.instance.add_custom_words(missing_words)
        for word in missing_words:
            with self.subTest(word=word, is_present=True, type='After Adding Custom Words'):
                got = self.instance.get_anagrams(word)
                self.assertTrue(len(got) > 0)

    def test_all_new(self):
        self.instance = AnagramGenerator()
        words_testable = {'arteezmis': False, 'misrateez': False, 'maeseztri': False, 'amseeztir': False}
        missing_words = []
        for word, is_present in words_testable.items():
            with self.subTest(word=word, is_present=is_present, type='Before Adding Custom Words'):
                got = self.instance.get_anagrams(word)
                if is_present:
                    self.assertTrue(len(got) > 0)
                else:
                    self.assertEqual(len(got), 0)
                    missing_words += word,

        self.instance.add_custom_words(missing_words)
        for word in missing_words:
            with self.subTest(word=word, is_present=True, type='After Adding Custom Words'):
                got = self.instance.get_anagrams(word)
                self.assertTrue(len(got) > 0)

if __name__ == '__main__':
    unittest.main()
