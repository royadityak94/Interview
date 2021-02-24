#!/usr/bin/python3
from character_tree import CharacterMap
from utilities import fetch_dictionary_file, persist_dictionary_file, fetch_working_variables, fetch_dictionary_information, is_non_zero_file
import argparse
import logging
import os
import mmap

def add_new_words(new_words):
    """Module to support custom new words into the dictionary
    """
    # Fetch the dictionary
    dict_file_path = fetch_dictionary_information()
    character_dictionary = fetch_dictionary_file(dict_file_path)
    
    for word in new_words:
        if len(word):
            chars = word.lower()
            character_dictionary.update({chars: CharacterMap(chars)})
    try:
        persist_dictionary_file(character_dictionary, dict_file_path)
    except Exception as ex: 
        print ("The process couldn't complete.")
        raise Exception(ex)
    return

if __name__ == '__main__':
    # Setting up the logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # Setting up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "-f",
            "--filepath",
            help= 'Input File Path (Relative/Absolute)',
            type= str,
            default= '../working/new_words.txt'
        )
    parser.add_argument(
            "-i",
            "--items",
            help= "Comma Separated New Words",
            type=str,
            default = ''
        )
    args = parser.parse_args()
    if len(args.items):
        logger.info('Skipping file path {file_path} as the new words '
                    + 'will be picked from the array: {array_items}'.format(
                    file_path=args.filepath, array_items=args.items))
        add_new_words(args.items.split(','))
    else:
        logger.info('Using {file_path} to load new words.'.format(file_path=args.filepath))
        assert os.path.exists(args.filepath), \
            "File not found in the input path: {file_path}".format(args.filepath)
        if is_non_zero_file(args.filepath):
            with open(args.filepath, mode='r', encoding='utf-8') as file_obj:
                with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj:
                    contents_arr = str(mmap_obj.read(), 'utf-8').split('\n')
                    add_new_words(contents_arr)
            # Empty the file contents
            open(args.filepath, "w").close()
        else:
            logger.warning('Empty file, quitting!')