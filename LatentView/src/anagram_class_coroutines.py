#!/usr/bin/python3

# Loading requisite modules
from collections import defaultdict
from utilities import fetch_word_list, formatted_strings
from itertools import tee, chain
import argparse
import logging

def coroutine(genFunc):
    def reurnValue(*args, **kwargs):
        handler = genFunc(*args, **kwargs)
        handler.send(None)
        return handler
    return reurnValue

class AnagramGenerator:
    """Anagram class uses coroutine that supports fetch and new word additions

    Python class utility to support Anagram usage across large set of users, word dictionaries

    Methods
    ----------
        - get_anagrams
            Parameters
            ----------
                string*: input string for which the anagram is requested
                maximum_size: maximum number of anagrams to be returned (default: None)
            Returns
            -------
                generated_anagrams : List holding anagram strings
        - add_custom_words
            Parameters
            ----------
                new_words*: List holding anagram strings to be added to the dictionary
            Returns
            -------
                None
    (* - Required parameters)
    """
    def __init__(self, word_list='nltk', file_path=None, logger=None):
        self.mapper = defaultdict(set)
        self.logger = logger
        self.data = fetch_word_list(word_list, file_path, logger)
        self.dictionary = iter(())
        self.chainer(self.data)

    def fetch_iterator(self):
        self.dictionary, bookmark = tee(self.dictionary)
        return bookmark

    def chainer(self, data):
        sorted_merged = self.anagram(self.merge_words())
        inventory = self.leaves_inventory(sorted_merged)
        inventory.send(data)
        filter_lambda = lambda item: len(item[1]) > 1
        self.dictionary = chain(self.dictionary, filter(filter_lambda, self.mapper.items()))

    @staticmethod
    def get_sorted_word(word):
        return ''.join(sorted(word))

    @coroutine
    def merge_words(self):
        while True:
            sorted_words = yield
            for word, anagram in sorted_words:
                self.mapper[word].add(anagram)

    @coroutine
    def leaves_inventory(self, handler):
        while True:
            words = yield
            for word in words:
                handler.send([self.get_sorted_word(word), word])
            handler.send('END')

    @coroutine
    def anagram(self, handler):
        generated_anagrams = list()
        while True:
            word = yield
            if word == 'END':
                handler.send(generated_anagrams)
            generated_anagrams += word,

    @staticmethod
    def format_return_anagrams(string, anagram_list, maximum_size):
        if not maximum_size:
            maximum_size =  float('inf')
        appended_words = list()
        for anagram_ in anagram_list:
            if anagram_ != string:
                appended_words += anagram_,
                if len(appended_words) == maximum_size:
                    break
        return appended_words

    def get_anagrams(self, string, maximum_size=None):
        assert maximum_size is None or maximum_size > 0, "Maximum Size can either be None or greater than 0"
        if not string.isalpha():
            return list()
        current = self.fetch_iterator()
        base_string = self.get_sorted_word(string.lower())
        done_exploring = False
        while not done_exploring:
            try:
                grouped_elements = next(current)
                if grouped_elements[0] == base_string:
                    return self.format_return_anagrams(string, grouped_elements[1], maximum_size)
            except StopIteration:
                done_exploring = True
        return list()

    def add_custom_words(self, new_words):
        formatted_words = formatted_strings(new_words)
        self.chainer(formatted_words)

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
    parser_input = parser.add_argument(
            "-d",
            "--word_list",
            help= 'Suport for custom data list',
            type= str,
            default= 'nltk'
        )
    parser_input = parser.add_argument(
            "-f",
            "--file_path",
            help= 'Suport for custom file path to load data from',
            type= str,
            default= None
        )
    args = parser.parse_args()
    if not args.input:
        raise argparse.ArgumentError(parser_input, 'Missing input or input cannot be empty string')

    anagram_gen = AnagramGenerator(args.word_list, args.file_path)
    print ("Found anagrams: ", end= '')
    for idx, anagram in enumerate(anagram_gen.get_anagrams(args.input)):
        if idx:
            print (', ', end= '')
        print ('(%d) %s' % (idx+1, anagram), end= '')
    print ()
