#!/usr/bin/python3
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
from utilities import formatted_strings

# Helper module to unit test formatted_strings(input_lst)
class TestFormattedStrings(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        pass
        
    @classmethod
    def tearDownClass(self):
        pass
        
    def test_default(self):
        input_list = ['ardent', 'brew', '2#d', ':sft', ',sdjn,', '@#,%absg', 'car']
        self.assertEqual(formatted_strings(input_list), ['ardent', 'brew', 'car'])
    
    def test_nocorrupt(self):
        input_list = ['ardent', 'brew', 'erx', 'sft', 'sdjn', 'absg', 'car']
        self.assertEqual(formatted_strings(input_list), input_list)
    
    def test_all_butone_corrupt(self):
        input_list = ['arda2dcx2ent', 'brew', '2#d', ':sft', ',sdjn,', '@#,%absg', 'c,ar']
        self.assertEqual(formatted_strings(input_list), ['brew'])
    
    def test_empty_file(self):
        input_list = []
        self.assertEqual(formatted_strings(input_list), [])
        
    def test_total_corrupt(self):
        input_list = ['ardent2', 'bre1w', '2#d', ':sft', ',sdjn,', '@#,%absg', 'c2ar']
        self.assertEqual(formatted_strings(input_list), [])



if __name__ == '__main__':
    unittest.main()