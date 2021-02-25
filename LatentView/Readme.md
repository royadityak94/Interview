# Drivers Activities Reporting
-------
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

## Problem Statement (Brief) - Anagram (Word) Generator:

Two given words are anagrams of each other if it's possible to permutate the order of characters in one of them in a bid to obtain the other. For example, listen and silent is anagrams of each other. In this problem statement,
we have limited our purview to only word anagrams. However, phrases/sentence anagram is also possible by ignoring spaces or capitalization, etc. For example, "Clint Eastwood" and "old west action" are anagrams.

An Anagram is a word or phrase made by rearranging the letters of another word or phrase. For example, "midterm" and "trimmed" are anagrams. If you ignore spaces and capitalization, a phrase is an anagram of another word or phrase.

### Example input (logical flow):

```
Get 'loop'
Get 'loop', 2
Get 'berzentini'
Add ['berzentini', 'brezentini', 'beeriizntn', 'beerzntnnii']
Get 'berzentini'
Get 'berzentini', 1
```

### Expected output (corresponding output):

```
loop, polo, pool
loop, polo

brezentini, beeriizntn, beerzntnnii
brezentini
```

## Explanation:
We have used 'nltk' as our word-dictionary, but the implementation makes it possible to use any dictionary or even file-based load. The first input 'loop' has several well-known word anagrams like the loop, polo, pool. The second input limits the number of returned anagrams to 2. The third input requests anagram for an inexistent word 'berzentini'. So, no anagrams are returned. However, we then proceed to add 'berzentini' and its known word anagrams to the dictionary, following which we can support anagram request on 'berzentini'.

The scenario of supporting custom words is pretty common across a domain, industry-specific applications like health-sciences or specific company-specific dialects like 'googleyness', etc.


## Solution Approaches:

From the problem statement, several assumptions can be levied, <ins>the most important of which are enumerated below</ins>:

```
(A) The design of the solution has to be scalable, dynamic key/value store (constant time lookup), wherein the keys are guaranteed to be a simple data structure (string).
(B) The designed solution has to support frequent get on the keys.
(C) Only single words anagrams need to be considered with a weight of 1. We have left-out sentence/phrase anagram or probabilistic/weighted scoring. Though such implementations are as well pretty well documented.
(D) We want to support domain-specific new word additions. Our implementation doesn't support new word removal, however as such pursuits are far-limited, such could be easily achieved with the reloading of the dictionary with undesirable words removed.
(E) We support only the exact anagram, i.e., the character count in the anagram and the input string are equal. Our implementation is easily extendible to approximate anagrams.
```

## Solution-1: Single large word file supported anagram generation on the fly

### Approach: 1
In such an implementation, we could simply load the word file (that contains all the words in a line-delimited fashion) and accept an input string argument, following which we iterate over all the words in the file sort them alphabetically and compare if the sorted word is same as the sorted input string, and we simply return all matched combinations.

<b> Complexity: </b> The time complexity is upper bounded by O(NMlogM), where N is the total words in the file, M is the maximum length of a word. The sorting of the word is performed in O(MLogM) time and O(1) space. The space complexity is O(k), where k is the number of matched words.

### Approach: 2

The second approach is to load the word file, and generate all permutations of the input string, and verifying if they exist in the word file. All matched words are then returned.

<b> Complexity: </b> The time complexity is upper bounded by O(N*(2^M)), where N is the total words in the file, M is the length of the input word. We spend O(2^M) time generating all permutations and for each permutation, we spend at most O(N) time in lookup. Though more unlikely, if the order of N and M are similar, the average time complexity is given by Catalan Number as O((4^M)/(N^.5)). The space complexity is O(k), where k is the number of matched words.

### Solution-2: Using Letter Inventory from processed word file

<b>Reference File:</b> `character_tree.py` <br/>

In this approach, we maintain active character counts from a-z of each letter in the text using a CharacterMap object that stores the words as a key and the CharacterMap object corresponding to the count of characters of that word. The CharacterMap supports setting character count, fetching count of a character, and even pruning over another CharacterMap. During runtime, making use of this abstraction, we use tree pruning to form remaining letter groups by subtracting the CharacterMap corresponding to a given word from the remaining words. The final result is built a single word at a time. Previously, we have mentioned the possibility of supporting approximate anagrams, which can be easily accomplished at this stage using backtracking and making two recursive calls using the current word and without the current word.

As the CharacterMap uses a key/value store, we have used a built-in dictionary for its thread-safety. Other data structures into consideration included [shelve](#https://docs.python.org/3/library/shelve.html), [chest](#https://github.com/blaze/chest). However as both of them are not well suited for small key-value pair use-cases and pose significant concern on their multiprocess safety, we believe the built-in dictionary is well reasoned on commodity hardware and size of the current dataset.

<b> Complexity: </b> The time complexity of the system is upper bounded by O(NLogM) where N is the total words in the file, M is the length of the input word. The space complexity of the system is O(N) in maintaining an active dictionary.

On another note, I was tempted to evaluate the idea of using open-source dynamic key-value stores like Etcd, Zookeeper, Redis, etc. Or, a full-fledged open-source key/value DBs like BerkeleyDB, etc. that would support efficient handling of the disk-space. However, given our existing assumptions, imbibing complexities arising out of distributed technologies and their inherent tradeoffs was beyond our affordability from the requisite application. I believe our design choice is well-reasoned, optimal for large-scale usage.

### Setup

- Python 3 (>=3.5)
- Create an appropriate environment (if deemed suitable)
```bash
conda create -n <env_name> python=<python_env>
ex: conda create -n test_anagrams python=3.7.9
```
- Install the required packages
```bash
pip install -r requirements.txt
or
python setup.py
```
- First, create the dictionary by running `bash python character_tree.py`. The utility supports a bunch of other access patterns, the details of which can be synthesized from the actual implementations.
- To run the test folder, navigate to ```bash src/tests ``` folder, and run any of the `test_*.py` files as ```bash python test_*.py```
- To run all the tests, `bash python -m unittest *`
- To run the actual code files directly from command line, navigate to the src directory and run:
```bash
python <file_name.py> -i <input_dir> -o <output_dir>
ex:
python anagram_generator.py -s loop
```
### Project Structure
```
project_name
   +-- README.md
   +-- environment.properties
   +-- .gitignore
   +-- setup.py
   +-- src
   |   +-- add_custom_words
   |   +-- anagram_class
   |   +-- anagram_generator
   |   +-- character_tree
   |   +-- utilities
   +-- tests
   |   +-- *unittest*
   |   +-- *functionaltest*
   +-- working
   |   +-- shelve_dict.pickle
 ```

N.B: The working directory `working` hosts the generated dictionary file. The testing utility as well independently generates, destroys files (as required) in their execution lifetime.

### Estimated Developmental Effort:

```
Development: 2.5-3 hours
Testing: 3 hours
Other Logistics (Formatting, Commenting, Documentation): 4 hours
```

### Thank-you Note

Thank you for your effort, time in reading the Readme file and thereby my other code segments. Should you have suggestions/advice on anything about the code piece, please reach out: [email](#mailto:p.adityak.roy@gmail.com).

Github Repo: [@royadityak94](#https://github.com/royadityak94), [@royadityak](#https://github.com/royadityak)
