import re
import pickle

def build(file):
    dict = {}
    f = open(file, 'r', encoding='utf-8')
    content = f.readlines()
    f.close()
    regex_word = re.compile(r'\w+')
    for line in content:
        line = line.lower()
        words = re.findall(regex_word, line)
        words = map(lambda word: word.lower(), words)
        for word in words:
            dict.setdefault(word, 0)
            dict[word] += 1

    return dict

if __name__ == '__main__':
    dict = build('WordSegmenation.txt')
    with open('word_dict.txt', 'wb') as f:
        pickle.dump(dict, f)

