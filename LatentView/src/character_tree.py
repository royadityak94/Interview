#!/usr/bin/python3
import logging
import argparse
from utilities import fetch_dictionary_information, create_dictionary, load_data_from_file
import os
from nltk.corpus import words

class CharacterMap:
    """Word mapper to coordinate letters of a word
    """
    
    def __init__(self, word=''):
        self.start = ord('a')
        self.bound = ord('z') - self.start + 1
        self.mapper = [0] * self.bound
        self.len = len(word) + 1
        if word.isalpha():
            for ch in word.lower():
                self.mapper[ord(ch) - self.start] += 1
    
    # Getter module
    def getter(self, ch):
        return self.mapper[ord(ch) - self.start]
    
    # Setter module
    def setter(self, ch, current):
        self.len += current - self.mapper[ord(ch) - self.start]
        self.mapper[ord(ch) - self.start] = current
        return
    
    # Recreate mapper class by intersecting current and given CharacterMap instances
    def remove(self, other):
        new_mapper = CharacterMap('')
        for itr in range(self.start, self.start+self.bound):
            ch = chr(itr)
            intersect = self.getter(ch) - other.getter(ch)
            if intersect < 0:
                return None
            new_mapper.setter(ch, intersect)
        return new_mapper
    
    # Dunder for length of the CharacterMap
    def __len__(self):
        return self.len
    
def create_charmap_dictionary(input_data='nltk', file_path=None, logger=None):
    data_list = None
    if file_path or input_data != 'nltk':
        if logger:
            logger.info('Using File Path {filepath} to load the data'.format(filepath= file_path))
        assert os.path.exists(file_path), "File not found in the file path"
        data_list = load_data_from_file(file_path)
        # Emptying the input file contents 
        open(args.file, "w").close()

    else:
        if logger:
            logger.info('Using NLTK Library to load the data')
        data_list = frozenset(words.words())
    assert data_list is not None, "Data List is empty, nothing to proceed with!"

    # Fetch the dictionary
    dict_file_path = fetch_dictionary_information()

    # Creating and Persisting the dictionary
    create_dictionary(data_list, dict_file_path, CharacterMap)
    return dict_file_path

if __name__ == '__main__':
    # setting up the logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    # Setting up the argument parser
    parser = argparse.ArgumentParser()
    parser_input = parser.add_argument(
            "-i",
            "--input",
            help= 'input string for which anagrams are requested',
            type= str,
            default= 'nltk'
        )
    parser_input = parser.add_argument(
            "-f",
            "--file",
            help= 'input file path (for data load from file)',
            type= str
        )
    args = parser.parse_args() #
    file_path = create_charmap_dictionary(args.input, args.file, logger)
    logger.info("Successfully loaded dictionary at {file_path}".format(file_path= file_path))
