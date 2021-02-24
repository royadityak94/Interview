#!/usr/bin/python3
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


import unittest
from anagram_class import Anagram
from character_tree import CharacterMap

class TestGetterModules(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.instance = Anagram()

    @classmethod
    def tearDownClass(self):
        del self.instance
    
    def test_fetch_anagrams_loop(self):
        expected = ['polo', 'pool']
        got = sorted(self.instance.get_anagrams('loop'))
        self.assertEqual(expected, got)
    
    def test_fetch_anagrams_loop_with_limit(self):
        expected = ['polo']
        got = sorted(self.instance.get_anagrams('loop', 1))
        self.assertEqual(expected, got)
    
    def test_fetch_anagrams_loops(self):
        expected = ['polos', 'sloop', 'spool']
        got = sorted(self.instance.get_anagrams('loops'))
        self.assertEqual(expected, got)
    
    def test_fetch_anagrams_loops_with_limit(self):
        expected = ['polos', 'sloop']
        got = sorted(self.instance.get_anagrams('loops', 2))
        self.assertEqual(expected, got)
    
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
        

class TestAddingCustomWords(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.instance = Anagram()

    @classmethod
    def tearDownClass(self):
        del self.instance
    
    def test_custom_words_nonexistent(self):
        new_words = 'byziitt,titizyb,zybitit,zybiitt'.split(',')
        for word in new_words:
            self.assertEqual(self.instance.get_anagrams(word), [])
        self.instance.add_custom_words(new_words, True)
        
        for idx, word in enumerate(new_words):
            expected = new_words[:]
            del expected[idx]
            self.assertEqual(self.instance.get_anagrams(word), expected)
    
    def test_custom_words_existent(self):
        expected = sorted(['artemis', 'misrate', 'maestri', 'amsetir'])
        self.assertNotEqual(sorted(self.instance.get_anagrams('msearit')), expected)
        self.instance.add_custom_words(['amsetir'], True)
        self.assertEqual(sorted(self.instance.get_anagrams('msearit')), expected)

if __name__ == '__main__':
    unittest.main()