#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script will create the two variables to be used for the coverage problem.
1 -- A universe of words (or elements) to be covered (~29,000)
    The elemnts are contained in the wds_universe set variable.
2 -- A universe of sets to choose from to cover the elements (~55,000)
    The sets are contained in the sets_universe list varaible.


Running this script should generate the reqired data. It is recomended to use 
the nltk.download() method to retrieve the data in order to automatically 
generate the file paths required to run the respective nltk methods.

This script requires the NLP package nltk is downloaded.

"""
import nltk

# nltk.download()
# Using the pop-up window, download the 
# "reuters" corpus in the corpora tab if not already installed


from nltk.corpus import reuters


def set_processing(list_set):
    cleaned_list = []
    i = 0
    while i < len(list_set):
        if not any(char.isdigit() for char in list_set[i]):
            if punctuation_check(list_set[i]):
                cleaned_list.append(list_set[i].lower())
        i += 1
    return set(cleaned_list)


def punctuation_check(inp_string):
    return \
        "." not in inp_string and \
        "'" not in inp_string and \
        len(inp_string) > 1


def sentence_processing(sentences):
    all_sets = []
    for i in range(len(sentences)):
        sentance_set = sentences[i]
        all_sets.append(set_processing(sentance_set))
    return all_sets


# PART 1
# Creating a set of all words representing my universe
wds = set(reuters.words())
list_set = list(wds)

# wds_universe represents all elemnts that can be "covered"
wds_universe = set_processing(list_set)

# PART 2
# Creating the "sets" from sentances
sentances = reuters.sents()
# paragraphs=reuters.paras()

# Which ever of the above two variables (sentances or paragraphs) I pass to the 
# sentanceProcessing function becomes my sets to choose.
sets_universe = sentence_processing(sentances)
