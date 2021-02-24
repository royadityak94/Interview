#!/usr/bin/python3
from character_tree import CharacterMap
from utilities import fetch_dictionary_file, fetch_dictionary_information
import argparse
import logging
import os
import mmap

def get_anagrams(input_string, maximum_size=None):
    # Fetch the dictionary
    dict_file_path = fetch_dictionary_information()
    character_dictionary = fetch_dictionary_file(dict_file_path)
    reconstructed = CharacterMap(input_string)
    generated_anagrams = list()
    for letters in character_dictionary.keys():
        if letters.isalpha() \
            and not letters == input_string \
            and not (len(letters) - len(input_string)) \
            and reconstructed.remove(character_dictionary.get(letters)):
            generated_anagrams += letters,
        
        if maximum_size and len(generated_anagrams) == maximum_size:
            break
    return generated_anagrams

if __name__ == '__main__':
    # Setting up the logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # Setting up the argument parser
    parser = argparse.ArgumentParser()
    parser_input = parser.add_argument(
            "-s",
            "--input",
            help= 'input string for which anagrams are requested',
            type= str
        )
    args = parser.parse_args()
    if not args.input:
        raise argparse.ArgumentError(parser_input, 'Missing input or input cannot be empty string')
       
    print ("Found anagrams: ", end= '')
    for idx, anagram in enumerate(get_anagrams(args.input.lower())):
        if idx:
            print (', ', end= '')
        print ('(%d) %s' % (idx+1, anagram), end= '')
    print ()