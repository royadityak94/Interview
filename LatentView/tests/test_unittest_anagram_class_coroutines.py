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
class TestGetterModules(unittest.TestCase):
    '''Test Modules for anagram_class.Anagram getter modules
    '''

    @classmethod
    def setUpClass(self):
        self.instance = AnagramGenerator()

    @classmethod
    def tearDownClass(self):
        del self.instance

    def test_fetch_anagrams_loop(self):
        expected = ['polo', 'pool']
        got = sorted(self.instance.get_anagrams('loop'))
        self.assertEqual(expected, got)

    def test_fetch_anagrams_loop_with_limit(self):
        expected = ['polo', 'pool']
        got = self.instance.get_anagrams('loop', 1)
        for anagram in got:
            self.assertTrue(anagram in expected)

    def test_fetch_anagrams_loops(self):
        expected = ['polos', 'sloop', 'spool']
        got = sorted(self.instance.get_anagrams('loops'))
        self.assertEqual(expected, got)

    def test_fetch_anagrams_loops_with_limit(self):
        expected = ['polos', 'sloop', 'spool']
        got = sorted(self.instance.get_anagrams('loops', 2))
        for anagram in got:
            self.assertTrue(anagram in expected)

    def test_fetch_anagram_aeprs(self):
        expected = sorted(['asper', 'spear', 'prase', 'parse', 'spare', 'spaer'])
        got = sorted(self.instance.get_anagrams('aeprs'))
        self.assertTrue(expected == got)

    def test_fetch_anagram_aeprs_length(self):
        got = sorted(self.instance.get_anagrams('aeprs'))
        self.assertTrue(len(got) == 6)

    def test_fetch_empty_anagram(self):
        expected = []
        got = sorted(self.instance.get_anagrams('blitzkrig'))
        self.assertEqual(expected, got)

# Helper module to unit test AnagramGenerator().add_custom_words(self, new_words)
class TestAddingCustomWords(unittest.TestCase):
    '''Test Modules for anagram_class.Anagram add_custom_words module
    '''

    @classmethod
    def setUpClass(self):
        self.instance = AnagramGenerator()

    @classmethod
    def tearDownClass(self):
        del self.instance

    def test_custom_words_nonexistent(self):
        new_words = sorted('byziitt,titizyb,zybitit,zybiitt'.split(','))
        for word in new_words:
            self.assertEqual(self.instance.get_anagrams(word), [])
        self.instance.add_custom_words(new_words)

        for idx, word in enumerate(new_words):
            expected = new_words[:]
            del expected[idx]
            self.assertEqual(sorted(self.instance.get_anagrams(word)), sorted(expected))

    def test_custom_words_existent(self):
        expected = sorted(['artemis', 'misrate', 'maestri', 'amsetir'])
        self.assertNotEqual(sorted(self.instance.get_anagrams('msearit')), expected)
        self.instance.add_custom_words(['amsetir'])
        self.assertEqual(sorted(self.instance.get_anagrams('msearit')), expected)

if __name__ == '__main__':
    unittest.main()
