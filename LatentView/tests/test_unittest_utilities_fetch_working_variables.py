#!/usr/bin/python3
# Adding src code to the test folder path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Loading the required packages
import unittest
from utilities import fetch_working_variables
from configparser import NoSectionError

# Helper module to unit test fetch_working_variables(properties_var, group_name)
class TestFetchWorkingVariables(unittest.TestCase):
    '''Test Modules for utilities.fetch_working_variables
    '''

    @classmethod
    def setUpClass(self):
        self.properties = '../environment.properties'
        self.group = 'WorkingVariables'
        self.expected = {'working.dir': '../working'}

    @classmethod
    def tearDownClass(self):
        del self.properties
        del self.group
        del self.expected

    def test_default(self):
        self.assertEqual(fetch_working_variables(self.properties, self.group), self.expected)

    def test_missing_properties(self):
        with self.assertRaises(AssertionError) as context:
            fetch_working_variables(None, self.group)
        self.assertTrue('Property Variable (properties_var) cannot be empty' in str(context.exception))

    def test_missing_group(self):
        with self.assertRaises(AssertionError) as context:
            fetch_working_variables(self.properties, None)
        self.assertTrue('Group Name Variable (group_name) cannot be empty' in str(context.exception))

    def test_missing_path(self):
        with self.assertRaises(FileNotFoundError) as context:
            fetch_working_variables('../work', self.group)
        self.assertTrue('No such file or directory' in str(context.exception))
        self.assertEqual(context.exception.errno, 2)

    def test_missing_section(self):
        with self.assertRaises(NoSectionError) as context:
            fetch_working_variables(self.properties, 'WorkingVariables2')
        self.assertTrue('Missing requested section in the properties file' in str(context.exception))

if __name__ == '__main__':
    unittest.main()
