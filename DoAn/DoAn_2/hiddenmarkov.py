from copy import deepcopy


def loop_each_sentence(**kwargs):
    for sample in kwargs['data']:
        kwargs['sample'] = sample
        kwargs['func'](**kwargs)


def build(**kwargs):
    index = 1 if kwargs['type'] == 'tag' else 0
    for features in kwargs['sample']:
        element = features[index]
        if element not in kwargs['container']:
            kwargs['container'].append(element)


def count_tag2word(**kwargs):
    for features in kwargs['sample']:
        word = features[0]
        tag = features[1]
        kwargs['container'][tag][word] += 1


def count_tag2tag(**kwargs):
    for i in range(0, len(kwargs['sample'])):
        if i == 0:
            prev_tag = '<s>'
        else:
            prev_tag = kwargs['sample'][i - 1][1]
        curr_tag = kwargs['sample'][i][1]
        kwargs['container'][prev_tag][curr_tag] += 1


def caculate(table):
    # smoothing (laplace)
    for cur_tag in table:
        for next_tag in table[cur_tag]:
            table[cur_tag][next_tag] += 1

    # caculate frequency
    for curr_tag in table:
        total = sum(table[curr_tag].values())
        for next_tag in table[curr_tag]:
            table[curr_tag][next_tag] /= total


def pretty_print(table):
    for tag in table:
        print(tag, table[tag])


class my_hidden_markov:
    tag2word = {}
    tag2tag = {}
    words = []
    tags = []

    def train(self, data):
        tags = self.tags
        loop_each_sentence(data=data, func=build, container=tags, type='tag')

        words = self.words
        loop_each_sentence(data=data, func=build, container=words, type='word')

        self.tag2tag['<s>'] = {tag: 0 for tag in tags}
        for tag in tags: self.tag2tag[tag] = {tag: 0 for tag in tags}
        loop_each_sentence(data=data, func=count_tag2tag, container=self.tag2tag)
        caculate(self.tag2tag)

        for tag in tags: self.tag2word[tag] = {word: 0 for word in words}
        loop_each_sentence(data=data, func=count_tag2word, container=self.tag2word)

    def predict(self, words):

        tags = self.tags
        dict_words = self.words
        tag2word = deepcopy(self.tag2word)
        tag2tag = deepcopy(self.tag2tag)

        checked_words = []
        num_Unknown = 0
        for word in words:
            if word not in dict_words:
                num_Unknown += 1
                unknown_word = 'Unknown_' + str(num_Unknown)
                for tag in tags: tag2word[tag][unknown_word] = 0
                checked_words.append(unknown_word)
            else:
                checked_words.append(word)
        caculate(tag2word)

        prob_paths = [tag2tag['<s>'][tag] * tag2word[tag][checked_words[0]] for tag in tags]
        paths = [[tag] for tag in tags]
        for word in checked_words[1:]:
            new_prob_paths = []
            new_paths = []
            for tag in tags:
                max_prob_path = -1
                for i, prob_path in enumerate(prob_paths):
                    prob_tag2word = tag2word[tag].get(word, 1)
                    prob_tag2tag = tag2tag[tags[i]][tag]
                    new_prob_path = prob_path * prob_tag2tag * prob_tag2word
                    if new_prob_path > max_prob_path:
                        max_prob_path = new_prob_path
                        pre_path = paths[i]
                new_prob_paths.append(max_prob_path)
                new_paths.append(pre_path + [tag])
            prob_paths = new_prob_paths
            paths = new_paths




        return list(zip(checked_words, paths[prob_paths.index(max(prob_paths))]))

    def score(self, data):

        acc = []
        for sample in data:
            words, tags = zip(*sample)
            words, pre_tags = zip(*self.predict(words))
            N = len(tags)
            acc.append(sum(1 if tags[i] == pre_tags[i] else 0 for i in range(N)) / N)

        mean_acc = sum(acc) / len(acc)

        return  mean_acc






if __name__ == '__main__':
    import pickle

    with open('data.txt', 'rb') as f:
        data = pickle.load(f)

    # data = [[('Lan', 'NNP'), ('day', 'VB'), ('con', 'UN'), ('sao', 'NN'), ('hot', 'VB')],
    #         [('Lan', 'NNP'), ('va', 'CC'), ('ban', 'NN'), ('hoc', 'VB'), ('bai', 'NN')]]

    # data = [[['con', 'UN'], ['mèo', 'NN'], ['trèo', 'VB'], ['cây', 'UN'], ['cau', 'NN']], [['con', 'UN'], ['chuột',
    # 'NN'], ['trèo', 'VB'], ['cây', 'UN'], ['cau', 'NN']], [['con', 'UN'], ['chuột', 'NN'], ['hỏi', 'VB'], ['con',
    # 'UN'], ['mèo', 'NN']], [['con', 'UN'], ['trèo', 'VB'], ['là', 'VB'], ['con', 'UN'], ['nào', 'PRP']]]

    my_model = my_hidden_markov()
    my_model.train(data[0:35])

    print(my_model.score(data[35:]))

