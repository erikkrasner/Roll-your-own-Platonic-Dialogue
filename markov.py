#coding=utf-8
import re
import random

########
# A data structure that keeps track of Markov chains
# in a body of text. "data" is a fixed-size list of dictionaries.
# data[n] contains a dictionary associating n-tuples of words
# found in the text with a probability distribution of the words that
# follow them. The lookup() function takes a tuple of words and returns
# an associated word chosen according to the probability distribution.
#######
class MarkovCorpus:
    def __init__(self, order):
        self.order = order
        self.data = []
        for i in range(order + 1):
            self.data.append({})
    # Associate a sequence of words with the word that follows it.
    #  If the sequence is length n, for k=0..n-1 do the same for the last k
    #  words in the sequence.
    def add(self, word_tuple, word):
        row = self.data[len(word_tuple)]
        if not word_tuple in row.keys():
            row[word_tuple] = {word:1}
        elif not word in row[word_tuple].keys():
            row[word_tuple][word] = 1
        else:
            row[word_tuple][word] += 1
        if word_tuple != ():
            if (word != "\0") | (len(word_tuple) != 1):
                    self.add(word_tuple[1:], word)
    # If the word tuple is a key, return a random associated word.
    #  Else return a random word associated with all but the first
    #  word in the tuple.
    def lookup(self, word_tuple):
        row = self.data[len(word_tuple)]
        if (word_tuple == ()) | (word_tuple in row.keys()):
            return self.choose_randomly(word_tuple)
        if word_tuple[0] == "\0":
            return "\0"
        return self.lookup(word_tuple[1:])
    # For a given sequence of words, choose a word from among the
    #  words associated with it, according to the probability of
    #  finding it in the original text.
    def choose_randomly(self, word_tuple):
        sum = 0
        probs = self.data[len(word_tuple)][word_tuple]
        for word, count in probs.iteritems():
            sum += count
        choice = random.randint(0,sum)
        sum = 0
        for word, count in probs.iteritems():
            sum += count
            if sum >= choice:
                return word
########
# Takes in natural text, tokenizes it into words and
#  feeds it to a MarkovCorpus.
########
class MarkovReader:
    def __init__(self, corpus):
        self.corpus = corpus
    # For every sequence corpus.order words in a given string,
    #  associate that sequence with the word that follows it
    #  in a MarkovCorpus.
    def read(self, string, order):
        words = self.tokenize(string)
        word_tuple = ()
        for word in words:
            self.corpus.add(word_tuple, word)
            if len(word_tuple) < order:
                word_tuple += word,
            else: word_tuple = word_tuple[1:] + (word,)
        for i in range(order):
            self.corpus.add(word_tuple, word)
            word_tuple = word_tuple[1:]
    # Split a string by spaces. Call breakdown() to sub-split
    #  it by punctuation marks.
    def tokenize(self, string):
        tokens = [" "] # Denotes the beginning of a document - guaranteed not to be a token itself
        for word in string.split():
            tokens += self.breakdown(word)
        tokens += "\0" # Denotes the end of a document
        return tokens
    # Split a word into strings of alphanumeric and punctuation
    #  characters. I chose to do this because I like to treat
    #  punctuation marks as separate syntactic units - i.e. when the
    #  text generator runs into "abc13", I want it to choose whether
    #  a comma or a period will immediately follow it.
    def breakdown(self, word):
        word_tokens = []
        alphanum = re.compile('\A\w+')
        punctuation = re.compile('\A\W+')
        while(word != ""):
            begin_match = alphanum.match(word)
            if not begin_match:
                begin_match = punctuation.match(word)
            word_tokens.append(begin_match.group())
            pattern_end = begin_match.end()
            word = word[pattern_end:]
        return word_tokens

######
# Generates a document according to the statistical
#  distribution described in a MarkovCorpus.
######
class MarkovWriter:
    def __init__(self, corpus):
        self.corpus = corpus
    # Keep generating tokens according to the rules described in
    #  a MarkovCorpus until you reach an end-of-document token,
    #  then return them all in one string.
    def write(self, order):
        token_list = []
        next_token = "garbage" # Immediately overwritten
        while(next_token != "\0"):
            word_tuple = tuple(token_list[-order:]) if order != 0 else ()
            next_token = self.corpus.lookup(word_tuple)
            token_list.append(next_token)
        token_list = token_list[1:-1]
        token_list[0] = token_list[0].capitalize()
        markov_string = ""
        for token in token_list:
            if (re.match('\A\w',token) != None) & (markov_string != ""):
                markov_string += " "
            markov_string += token
        return markov_string
