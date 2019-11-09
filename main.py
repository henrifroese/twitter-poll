# -*- coding: utf-8 -*-
"""
## Predicting political affiliation from Tweets
### Part I: getting data
1. Get recent tweets from German politicians, categorized by party
2. Tokenize and normalize the tweets
3. Transform tokens to usable Neural Network input (as "Bag of Words"-Vector)
"""

import numpy
import matplotlib.pyplot
from keras.layers import Dense, Dropout, ActivityRegularization
from keras.preprocessing.text import Tokenizer
from keras.engine.sequential import Sequential
from keras.optimizers import SGD
from keras.utils import to_categorical
from keras import regularizers


"""Function takes list of twitter usernames and return list of each user's content (tokenized) 
of their 100 most recent tweets (retweets are excluded)
"""


with open("data/vocab.txt", 'r') as vocab_file:
    vocab_file = vocab_file.readlines()
    vocab = [word.strip() for word in vocab_file]
    vocab = set(vocab)


def getlines(filename):
    with open(filename, 'r') as f:
        f.readline()
        f = f.readlines()
        li = list()
        for index, line in enumerate(f):
            if index == 60:
                break
            tokens = line.strip().split()
            tokens = [w for w in tokens if w in vocab]
            li.append(' '.join(tokens))
    return li


def getlines_test(filename):
    with open(filename, 'r') as f:
        f.readline()
        f = f.readlines()
        li = list()
        for index, line in enumerate(f):
            if index < 60:
                continue
            tokens = line.strip().split()
            tokens = [w for w in tokens if w in vocab]
            li.append(' '.join(tokens))
    return li


# Training data
afd_lines = getlines("data/tweets/afd_tokens.txt")
cdu_lines = getlines("data/tweets/cdu_tokens.txt")
fdp_lines = getlines("data/tweets/fdp_tokens.txt")
greens_lines = getlines("data/tweets/greens_tokens.txt")
linke_lines = getlines("data/tweets/linke_tokens.txt")
spd_lines = getlines("data/tweets/spd_tokens.txt")

tokenizer = Tokenizer()
all_lines = afd_lines + cdu_lines + fdp_lines + greens_lines + linke_lines + spd_lines

tokenizer.fit_on_texts(all_lines)


# Test data
afd_lines_test = getlines_test("data/tweets/afd_tokens.txt")
cdu_lines_test = getlines_test("data/tweets/cdu_tokens.txt")
fdp_lines_test = getlines_test("data/tweets/fdp_tokens.txt")
greens_lines_test = getlines_test("data/tweets/greens_tokens.txt")
linke_lines_test = getlines_test("data/tweets/linke_tokens.txt")
spd_lines_test = getlines_test("data/tweets/spd_tokens.txt")

all_lines_test = afd_lines_test + cdu_lines_test + fdp_lines_test + greens_lines_test + linke_lines_test + spd_lines_test


def model(encoding_mode, hidden_nodes, dropout_rate, learning_rate, epochs):
    # encode training data set
    Xtrain = tokenizer.texts_to_matrix(all_lines, mode=encoding_mode)
    print(Xtrain.shape)  


    # encode testing data set
    Xtest = tokenizer.texts_to_matrix(all_lines_test, mode=encoding_mode)
    print(Xtest.shape)  
    
    
    n_words = Xtest.shape[1]  # input size
    
    ytrain = numpy.array([0 for _ in range(60)] + [1 for _ in range(60)] + [2 for _ in range(60)] +
                         [3 for _ in range(60)] + [4 for _ in range(60)] + [5 for _ in range(60)])
    ytrain = to_categorical(ytrain)
    ytest = numpy.array([0 for _ in range(19)] + [1 for _ in range(22)] + [2 for _ in range(18)] +
                        [3 for _ in range(14)] + [4 for _ in range(3)] + [5 for _ in range(31)])
    ytest = to_categorical(ytest)
    
    model = Sequential()
    model.add(Dropout(dropout_rate))
    model.add(Dense(hidden_nodes, input_shape=(n_words,), activation='relu', kernel_initializer='he_uniform'))
    model.add(Dense(6, activation='softmax'))
    
    opt = SGD(lr=learning_rate, momentum=0.9)
    model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])
    
    history = model.fit(Xtrain, ytrain, validation_data=(Xtest, ytest), epochs=epochs, verbose=0)
    
    _, train_acc = model.evaluate(Xtrain, ytrain, verbose=0)
    _, test_acc = model.evaluate(Xtest, ytest, verbose=0)
    
    print("Train: %.3f, Test: %.3f" % (train_acc, test_acc))
    
    matplotlib.pyplot.subplot(211)
    matplotlib.pyplot.title('Loss')
    matplotlib.pyplot.plot(history.history['loss'], label='train')
    matplotlib.pyplot.plot(history.history['val_loss'], label='test')
    matplotlib.pyplot.legend()
    # plot accuracy during training
    matplotlib.pyplot.subplot(212)
    matplotlib.pyplot.title('Accuracy')
    matplotlib.pyplot.plot(history.history['accuracy'], label='train')
    matplotlib.pyplot.plot(history.history['val_accuracy'], label='test')
    matplotlib.pyplot.legend()
    matplotlib.pyplot.show()

    with open('data/performance.txt', 'a') as f:
        str_out = "encoding mode: " + str(encoding_mode) + " hidden nodes: " + str(hidden_nodes) + \
                " dropout rate: " + str(dropout_rate) + " learning rate: " + str(learning_rate) + \
                " epochs: " + str(epochs) + " Train: " + str(train_acc) + " Test: " + str(test_acc) + "\n"
        f.write(str_out)

model('freq', 5000, 0.5, 0.01, 800)
