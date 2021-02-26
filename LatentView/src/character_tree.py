#!/usr/bin/python3

# Loading requisite modules
import logging
import argparse
from utilities import fetch_dictionary_information, create_dictionary, load_data_from_file, fetch_word_list
import os


class CharacterMap:
    """Word mapper to coordinate letters of a word
    Methods
    ----------
        - getter
            Parameters
            ----------
                ch*: input character
            Returns
            -------
                'String': Frequency of the character
        - setter
            Parameters
            ----------
                ch*: input character
                current: Current Frequency
            Returns
            -------
                None
        - remove
            Parameters
            ----------
                other*: CharacterMap instance
            Returns
            -------
                new_mapper: CharacterMap instance
    (* - Required parameters)
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
    """Module to support character map dictitonary creation through method call/cli
    Parameters
    ----------
        input_data: The standard data list source to be used for dictionary (default: nltk)
        file_path: If the standard list source is a file, the path of such file (default: None)
        logger: Instance of custom logger (default: None)
    Returns
    -------
        dict_file_path : String holding the path where the dictionary file has been persisted
    (* - Required parameters)
    """
    data_list = fetch_word_list(input_data, file_path, logger)

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
