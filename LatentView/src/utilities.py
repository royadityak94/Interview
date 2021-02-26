#!/usr/bin/python3

# Loading requisite modules
from configparser import RawConfigParser, NoSectionError
import pickle
import errno
import os
import mmap
from nltk.corpus import words

def fetch_working_variables(properties_var, group_name):
    """Module to fetch working variables
    """
    assert properties_var, "Property Variable (properties_var) cannot be empty"
    assert group_name, "Group Name Variable (group_name) cannot be empty"

    if os.path.exists(properties_var):
        config = RawConfigParser()
        config.read(properties_var)
        try:
            return dict(config.items(group_name))
        except NoSectionError:
            raise NoSectionError("Missing requested section in the properties file")
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), properties_var)
    return

def is_non_zero_file(filepath):
    """Module to validate filepath and content presence
    """
    return os.path.isfile(filepath) and os.path.getsize(filepath) > 0

def fetch_dictionary_file(dict_file_path):
    """Module to fetch dictionary file from a given path
    """
    assert is_non_zero_file(dict_file_path), "Empty file, please proceed to load the dictionary first"
    with open(dict_file_path, 'rb') as handle:
        character_dictionary = pickle.load(handle)
    return character_dictionary

def persist_dictionary_file(character_dictionary, dict_file_path):
    """Module to persist dictionary file at a given path
    """
    # dict_file_dir = os.path.join(*dict_file_path.split('/')[:-1])
    dict_file_dir = dict_file_path[:len(dict_file_path) - dict_file_path[::-1].find('/')]
    if not os.path.exists(dict_file_dir):
        os.makedirs(dict_file_dir, exist_ok=True)

    with open(dict_file_path, 'wb') as handle:
        pickle.dump(character_dictionary, handle, protocol=pickle.HIGHEST_PROTOCOL)

def fetch_dictionary_information(properties=None, group = None):
    """Module to fetch dictionary information
    """
    if not properties:
        properties = '../environment.properties'
    if not group:
        group = 'WorkingVariables'
    environ_variables = fetch_working_variables(properties_var= properties, group_name= group)
    dict_file_path = os.path.join(environ_variables['working.dir'], 'shelve_dict.pickle')
    assert os.path.exists(dict_file_path), 'The dictionary file is missing!'
    return dict_file_path

def swap(i, j, array):
    """Module to swap array indexes
    """
    array[i], array[j] = array[j], array[i]

def formatted_strings(input_lst):
    """Module to pre-process input file contents
    """
    start = 0
    end = len(input_lst)-1
    while start < len(input_lst):
        if not input_lst[start].isalpha():
            swap(start, end, input_lst)
            input_lst.pop()
            end -= 1
        else:
            if not input_lst[start].islower():
                input_lst[start] = input_lst[start].lower()
            start += 1
    return input_lst

def load_data_from_file(file_path):
    """Module to load file data
    """
    assert os.path.exists(file_path), \
            "File not found in the input path: {file_path}".format(file_path)
    parsed_data = []
    with open(file_path, mode='r', encoding='utf-8') as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj:
            file_contents = str(mmap_obj.read(), 'utf-8').split('\n')
            parsed_data.extend(formatted_strings(file_contents))
    return frozenset(parsed_data)

def create_dictionary(data, dict_file_path, CharacterMap):
    """Module to create dictionary file
    """
    character_dictionary = dict()
    for word in data:
        chars = word.lower()
        character_dictionary.update({chars: CharacterMap(chars)})
    persist_dictionary_file(character_dictionary, dict_file_path)

def fetch_word_list(input_data='nltk', file_path=None, logger=None):
    """Module to fetch the relevant word_list from given input data or file_path
    """
    data_list = None
    if file_path or input_data != 'nltk':
        if logger:
            logger.info('Using File Path {filepath} to load the data'.format(filepath= file_path))
        assert os.path.exists(file_path), "File not found in the file path"
        data_list = load_data_from_file(file_path)
        # Emptying the input file contents
        open(file_path, "w").close()

    else:
        if input_data.lower() == 'demo':
            if logger:
                logger.info('Loading demo data')
            data_list = ['abc', 'acb', 'bca', 'iterl', 'Liter', 'elHlo', 'subessential', 'suitableness', 'hello', 'pool']
        elif input_data.lower() == 'nltk':
            if logger:
                logger.info('Using NLTK Library to load the data')
            data_list = words.words()
        else:
            raise Exception('The utility needs input data list to operate')
    assert data_list is not None, "Data List is empty, nothing to proceed with!"
    return frozenset(formatted_strings(data_list))
