import re
import pickle




def process(file='data1.txt'):
    f = open(file, 'r', encoding='utf-8')
    lines = f.readlines()
    f.close()
    samples = []
    regex_terms = re.compile(r'\w+|,|\.')
    f = open('proces_' + file, 'w', encoding='utf-8')
    for line in lines:
        if line.strip() == '':
            continue
        terms = re.findall(regex_terms, line)
        tags = ['None' for _ in range(len(terms))]
        sample = list(zip(terms, tags))
        f.write(str(sample) + '\n')
    f.close()


def foo(file='proces_data1.txt'):

    samples = []
    f = open(file, 'r', encoding='utf-8')
    content = f.readlines()
    f.close()
    for line in content:
        print(line)
        line = line.replace('\n', '')
        line = line.replace(' ', '')
        sample = eval(line)

        samples.append(sample)

    f = open('data.txt', 'wb')
    pickle.dump(samples, f)
    f.close()






if __name__ == '__main__':
    f = open('data.txt', 'rb')
    samples = pickle.load(f)
    f.close()
    print(len(samples))