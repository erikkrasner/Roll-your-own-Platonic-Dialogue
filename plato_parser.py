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
                    current_speech = line[speech_index:-1]
                    current_speaker = speaker_name
                else:
                    current_speech += line[:-1]
                    return speakers_and_words

def parse_standard_dialogue(file_name):
    dialogue = open(file_name,'r')
    speaker_list = get_speakers(dialogue)
    dialogue.next()
    speakers_and_words = get_speakers_and_words(dialogue, speaker_list)
    return speakers_and_words

standard_dialogues = ['cratylus', 'critias', 'crito', 'euthydemus', 'euthyphro', 'gorgias','ion','laches','meno', 'phaedrus', 'philebus','protagoras', 'sophist', 'statesman','theaetatus','timaeus']
