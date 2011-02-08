import pickle
from markov import *

class PlatoWriter:
    def filter_corpus(corpus, character_list):
        def subset(seq1,seq2):
            for elem in seq1:
                if elem not in seq2:
                    return False
            return True
        def filter_dict_by_key(condition, dictionary):
            new_dictionary = {}
            for key in dictionary:
                if condition(key):
                    new_dictionary[key] = dictionary[key]
            return new_dictionary
        subset_condition = lambda seq: subset(seq, character_list)
        new_corpus = MarkovCorpus(0)
        for row in corpus:
            new_row = filter_dict_by_key(subset_condition, row)
            for key in new_row:
                new_row[key] = filter(lambda w: w in character_list or w == '\0', new_row[key])
            new_corpus.append(new_row)
            new_corpus.order = corpus.order
        return new_corpus
