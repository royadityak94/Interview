#!/usr/bin/python3

# Loading requisite modules
from character_tree import CharacterMap
from utilities import fetch_dictionary_file, fetch_dictionary_information

class Anagram:
    """Anagram class that supports fetch and new word additions
    Class Utility to support Anagram usage across large set of users

    Methods
    ----------
        - get_anagrams
            Parameters
            ----------
                input_string*: input string for which the anagram is requested
                maximum_size: maximum number of anagrams to be returned (default: None)
            Returns
            -------
                generated_anagrams : List holding anagram strings
        - add_custom_words
            Parameters
            ----------
                new_words*: List holding anagram strings to be added to the dictionary
                local_only: Scope new word addition to only the current instance
                            and not the actual dictionary(default: False)
            Returns
            -------
                None
    (* - Required parameters)
    """
    def __init__(self):
        # Fetch the dictionary
        dict_file_path = fetch_dictionary_information()
        # Load the character map
        self.character_dictionary = fetch_dictionary_file(dict_file_path)

    def get_anagrams(self, input_string, maximum_size=None):
        if not input_string.isalpha():
            return list()
        reconstructed = CharacterMap(input_string.lower())
        generated_anagrams = list()
        for letters in self.character_dictionary.keys():
            if letters.isalpha() \
                and not letters == input_string \
                and not (len(letters) - len(input_string)) \
                and reconstructed.remove(self.character_dictionary.get(letters)):
                generated_anagrams += letters,

            if maximum_size and len(generated_anagrams) == maximum_size:
                break
        return generated_anagrams

    def add_custom_words(self, new_words, local_only=False):
        for word in new_words:
            if len(word):
                chars = word.lower()
                self.character_dictionary.update({chars: CharacterMap(chars)})
        if len(new_words) and not local_only:
            try:
                persist_dictionary_file(self.character_dictionary, dict_file_path)
            except Exception as ex:
                print ("The process couldn't complete.")
                raise Exception(ex)
        return
