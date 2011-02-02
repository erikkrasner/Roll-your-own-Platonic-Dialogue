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
