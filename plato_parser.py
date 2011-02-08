from markov import *
import pickle

def is_prefix(str1,str2):
    return len(str2) >= len(str1) and str2[:len(str1)].lower() == str1.lower()

def find_speaker(speaker_list,speaker_prefix):
    matches = filter(lambda speaker:is_prefix(speaker_prefix,speaker),speaker_list)
    if len(matches) == 0:
        return None
    return matches[0]

def get_speakers(file_object):
    speakers = []
    parsing_speakers = False
    for line in file_object:
        if not parsing_speakers and line == "Persons of the Dialogue\n":
            parsing_speakers = True
        elif parsing_speakers:
            if "-----" in line:
                break
            speakers.append(line[:line.index(",")] if "," in line else line[:-1])
    return speakers

def get_speakers_and_words(dialogue_file, speaker_list):
    def parse_speaker(line):
        if '. ' not in line:
            return (None, None)
        dot_space_index = line.index(". ")
        speaker = find_speaker(speaker_list, line[:dot_space_index])
        if speaker:
            return (speaker, dot_space_index + 2)
        return (None, None)
    speakers_and_words = {}
    speaker_sequence = ""
    for speaker in speaker_list:
        speakers_and_words[speaker] = []
        current_speech = ""
        current_speaker = None
        for line in dialogue_file:
            if "THE END" not in line and "-------" not in line:
                speaker_name, speech_index = parse_speaker(line)
                if speaker_name:
                    if current_speaker:
                        speakers_and_words[current_speaker].append(current_speech)
                        speaker_sequence += " " + current_speaker
                    else:
                        speaker_sequence = current_speaker
                    current_speech = line[speech_index:-1]
                    current_speaker = speaker_name
                else:
                    if current_speech[-1] != " ":
                        current_speech += " "
                    current_speech += line[:-1]
    return speakers_and_words

def parse_standard_dialogue(file_name):
    dialogue = open(file_name,'r')
    speaker_list = get_speakers(dialogue)
    dialogue.next()
    speakers_and_words = get_speakers_and_words(dialogue, speaker_list)
    return speakers_and_words

class SequenceMarkovReader(MarkovReader):
    def __init__(self,corpus):
        MarkovReader.__init__(self,corpus)
        self.sequence_counts = {}
    def read(self, string, order):
        def count(word_tuple):
            if word_tuple not in seen_already:
                if word_tuple in self.sequence_counts:
                    self.sequence_counts[word_tuple] += 1
                else:
                    self.sequence_counts[word_tuple] = 1
                seen_already.add(word_tuple)
                if word_tuple != ():
                    count(word_tuple[1:])
        words = self.tokenize(string)
        seen_already = set()
        word_tuple = ()
        for word in words:
            self.corpus.add(word_tuple, word)
            count(word_tuple)
            if len(word_tuple) < order:
                word_tuple += word,
            else: word_tuple = word_tuple[1:] + (word,)
        for i in range(order):
            self.corpus.add(word_tuple, word)
            count(word_tuple)
            word_tuple = word_tuple[1:]
    def normalize_counts(self):
        print self.sequence_counts
        for row in self.corpus:
            for word_tuple in row:
                word_table = row[word_tuple]
                count = self.sequence_counts[word_tuple]
                for word in word_table:
                    if word_table[word] % count == 0:
                        word_table[word] /= count
                    else:
                        word_table[word] /= count
                        word_table[word] += 1

if __name__ == '__main__':
    standard_dialogues = ['cratylus', 'critias', 'crito', 'euthydemus', 'euthyphro', 'gorgias','ion','laches','meno', 'phaedrus', 'philebus','protagoras', 'sophist', 'statesman','theaetatus','timaeus']
    speaker_markovs = {}
    speaker_markov_readers = {}
    sequence_markov = MarkovCorpus(3)
    sequence_markov_reader = SequenceMarkovReader(sequence_markov)
    for dialogue in standard_dialogues:
        speakers_and_words, speaker_sequence = parse_standard_dialogue("dialogues/%s.txt" % dialogue)
        for speaker in speakers_and_words:
            if speaker not in speaker_markovs:
                speaker_markovs[speaker] = MarkovCorpus(4)
                speaker_markov_readers[speaker] = MarkovReader(speaker_markovs[speaker])
            for words in speakers_and_words[speaker]:
                MarkovReader(speaker_markovs[speaker]).read(words,4)
        sequence_markov_reader.read(speaker_sequence, 3)
    sequence_markov_reader.normalize_counts()
    sequence_file = open("datafiles/sequence.dat",'w')
    pickle.dump(sequence_markov, sequence_file)
    for speaker in speaker_markovs:
        save_file = open("datafiles/%s.dat" % speaker,'w')
        pickle.dump(speaker_markovs[speaker],save_file)
