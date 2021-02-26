#!/usr/bin/python3

# Loading requisite modules
from character_tree import CharacterMap
from utilities import fetch_dictionary_file, fetch_dictionary_information, is_non_zero_file
import argparse
import logging
import os
import mmap

def get_anagrams(input_string, maximum_size=None):
    """Module to support stand-alone get anagrams helper utility
    Parameters
    ----------
        input_string*: input string for which the anagram is requested
        maximum_size: maximum number of anagrams to be returned (default: None)
    Returns
    -------
        generated_anagrams : List holding anagram strings
    (* - Required parameters)
    """
    if not input_string.isalpha():
        return list()
    # Fetch the dictionary
    dict_file_path = fetch_dictionary_information()
    character_dictionary = fetch_dictionary_file(dict_file_path)
    try:
        reconstructed = CharacterMap(input_string.lower())
        generated_anagrams = list()
        for letters in character_dictionary.keys():
            if letters.isalpha() \
                and not letters == input_string \
                and not (len(letters) - len(input_string)) \
                and reconstructed.remove(character_dictionary.get(letters)):
                generated_anagrams += letters,

            if maximum_size and len(generated_anagrams) == maximum_size:
                break
    except Exception as ex:
        raise Exception("The process couldn't complete: %s" % str(ex))
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
