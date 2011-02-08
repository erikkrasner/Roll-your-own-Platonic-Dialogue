import pickle
from markov import *

class PlatoWriter:
    def __init__(self, character_list):
        sequence_corpus = pickle.load(open('datafiles/sequence.dat','r'))
        sequence_corpus = self.filter_corpus(sequence_corpus, character_list)
        self.sequence_writer = MarkovWriter(sequence_corpus)
        self.speaker_writers = {}
        for speaker in character_list:
            if speaker == 'SOCRATES':
                #Socrates needs to be in two files to overcome 10MB Google App Engine limit
                soc_string = open('datafiles/SOCRATES1.dat','r').read() + open('datafiles/SOCRATES2.dat','r').read()
                speaker_corpus = pickle.loads(soc_string)
            else:
                speaker_corpus = pickle.load(open("datafiles/%s.dat" % speaker, 'r'))
            speaker_writers[speaker] = MarkovWriter(speaker_corpus)
    def write(self, order):
        sequence_string = self.sequence_writer.write(3)
        seqeunce = sequece_string.split()
        return map(lambda speaker: speaker_writers[speaker].write(order),sequence)
    def filter_corpus(self, corpus, character_list):
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
    
