def is_prefix(str1,str2):
    return len(str2) >= len(str1) and str2[:len(str1)] == str1

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

def parse_standard_dialogue(file_name):
    dialogue = open(file_name,'r')
    for line in dialogue:
        if '-----' in line:
            break
    dialogue.next()
    dialogue_string = ""
    dialogue_list = []
    for line in dialogue:
        if line != '\n':
            if dialogue_string:
                dialogue_string += ' '
            dialogue_string += line[:-1]
        else:
            dialogue_list.append(dialogue_string)
            dialogue_string = ""
    return dialogue_list

standard_dialogues = ['cratylus', 'critias', 'crito', 'euthydemus', 'euthyphro', 'gorgias','ion','laches','meno', 'phaedrus', 'philebus','protagoras', 'sophist', 'statesman','theaetatus','timaeus']
