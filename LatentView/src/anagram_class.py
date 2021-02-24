#!/usr/bin/python3
from character_tree import CharacterMap
from utilities import fetch_dictionary_file, fetch_dictionary_information

class Anagram:
    def __init__(self):
        # Fetch the dictionary
        dict_file_path = fetch_dictionary_information()
        # Load the character map
        self.character_dictionary = fetch_dictionary_file(dict_file_path)
    
    def get_anagrams(self, input_string, maximum_size=None):
        reconstructed = CharacterMap(input_string)
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