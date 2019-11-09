import linecache
from nltk.corpus import stopwords
import string
from string import punctuation
from os import listdir
from collections import Counter

vocab = Counter()


def process_directory(directory, vocab):

    for filename in listdir(directory):

        path = directory + '/' + filename

        add_doc_to_vocab(path, vocab)


def add_doc_to_vocab(filename, vocab):

    with open(filename, 'r') as f:
        for index, line in enumerate(f):
            if index == 60:
                break
            tokens = line.split()
            vocab.update(tokens)


process_directory('data/tweets', vocab)

# saving the vocab
vocab_list = [x for x in vocab if vocab[x] > 4]
with open('data/vocab.txt', 'w') as f:
    for word in vocab_list:
        f.write("%s\n" % word)
print(len(vocab))
print(len(vocab_list))