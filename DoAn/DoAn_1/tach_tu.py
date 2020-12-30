import subprocess
from matplotlib import image, pyplot
from numpy import asarray
import pickle
import re

def makeSymbols(dictionary):
    f = open('sym.txt', "wt", encoding='utf-8')
    i = 0
    f.write('# {}\n'.format(i))
    for word in dictionary:
        i += 1
        f.write("{} {}\n".format(word, i))
    f.close()


def WFSTSegmentation(dict, sent):
    words = sent.split()
    f = open("tmp.txt", "wt", encoding='utf-8')
    nwords = len(words)
    for i in range(nwords):
        for j in range(4):
            if i + j >= nwords:
                break
            word = words[i]
            for k in range(1, j + 1):
                word = word + "_" + words[i + k]
            weight = dict.get(word)
            if  weight is None:
                if j != 0:
                    continue
                dict[word] = 10000
                weight = 10000
                with open('sym.txt', 'a', encoding='utf-8') as f_1:
                    f_1.write(f'{word} {len(dict)}\n')
            f.write("{} {} {} {} {}\n".format(i, i + j + 1, word, word, weight))
    f.write("{}".format(nwords))
    f.close()

    process = subprocess.Popen(["fstcompile", "-isymbols=sym.txt", "-osymbols=sym.txt", "tmp.txt", "tmp.fst"])
    process.wait()
    process = subprocess.Popen(["fstdraw", "-portrait", "-isymbols=sym.txt", "-osymbols=sym.txt", "tmp.fst", "tmp.dot"])
    process.wait()
    process = subprocess.Popen(["dot", "-Tpng", "tmp.dot", "-otmp.png"])
    process.wait()
    img = image.imread("tmp.png")
    # pyplot.imshow(img)
    # pyplot.axis('off')
    # pyplot.show()

    process = subprocess.Popen(["fstshortestpath", "tmp.fst", "path.fst"])
    process.wait()
    process = subprocess.Popen(["fstdraw", "-portrait", "-isymbols=sym.txt", "-osymbols=sym.txt", "path.fst", "path.dot"])
    process.wait()
    process = subprocess.Popen(["dot", "-Tpng", "path.dot", "-opath.png"])
    process.wait()
    img = image.imread("path.png")
    # pyplot.imshow(img)
    # pyplot.axis('off')
    # pyplot.show()


def load_dict(file='word_dict.txt'):
    dict = {}
    with open(file, 'rb') as f:
        dict = pickle.load(f)
    return dict

def get_result(file='path.dot'):
    regex_words = re.compile(r'(\d+) -> \d+ \[label = \"(\w+)')
    f = open(file, 'r', encoding='utf-8')
    content = f.read()
    f.close()
    words = re.findall(regex_words, content)
    words.sort(key=lambda x: int(x[0]), reverse=True)

    index, words = zip(*words)

    sentence = ' '.join(words)

    return sentence
if __name__ == '__main__':
    dict = load_dict()
    s = 'phan le phu'

    makeSymbols(dict)
    WFSTSegmentation(dict, s)
    sentence = get_result()
    print(sentence)