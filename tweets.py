#@PydevCodeAnalysisIgnore
'''
Created on Nov 7, 2019

@author: henri
'''
import json
from TwitterSearch import *
import datetime
import linecache
import math
from nltk.corpus import stopwords
import string
from string import punctuation
from os import listdir
from collections import Counter
import numpy
import matplotlib.pyplot

import keyfile


def mainsearch(usernames, my_consumer_key = keyfile.consumer_key, my_consumer_secret = keyfile.consumer_secret,
              my_access_token = keyfile.access_token, my_access_token_secret = keyfile.access_token_secret):

    ts = TwitterSearch(
        consumer_key = my_consumer_key,
        consumer_secret = my_consumer_secret,
        access_token = my_access_token,
        access_token_secret = my_access_token_secret
     )

    tokens_all_users = list()

    for username in usernames:

        try:

            tuo = TwitterUserOrder(username)
            tuo.set_include_rts(False)  # ?
            # tuo.set_count(20) does not seem to work -> use enumerate

            tokens_user = list()

            for index, tweet in enumerate(ts.search_tweets_iterable(tuo)):

                tweet_content = tweet['text']
                table = str.maketrans('', '', string.punctuation)
                # tokenize and remove punctuation and lowercase 
                tweet_content = [word.translate(table).lower() for word in tweet_content.split()] 

                # remove non-alphanumeric and short words and filter out stop words
                stop_words = set(stopwords.words('german'))
                tweet_content = [word for word in tweet_content if word.isalpha() and len(word) > 2 and word not in stop_words]                

                tokens_user += tweet_content

                if index == 99:  # 100 tweets per user
                    break

        except TwitterSearchException as e:  # take care of errors
            print(e, username)

        tokens_all_users.append(tokens_user)

    return tokens_all_users  # list of lists (each list containing tokens of one user)


def singlesearch(username, my_consumer_key = keyfile.consumer_key, my_consumer_secret = keyfile.consumer_secret,
              my_access_token = keyfile.access_token, my_access_token_secret = keyfile.access_token_secret):

    ts = TwitterSearch(
        consumer_key = keyfile.consumer_key,
        consumer_secret = keyfile.consumer_secret,
        access_token = keyfile.access_token,
        access_token_secret = keyfile.access_token_secret
     )

    try:

        tuo = TwitterUserOrder(username)
        tuo.set_include_rts(False)  
        # tuo.set_count(20) does not seem to work -> use enumerate
    
        tokens_user = list()
    
        for index, tweet in enumerate(ts.search_tweets_iterable(tuo)):
    
        	tweet_content = tweet['text']
        	table = str.maketrans('', '', string.punctuation)
        	# tokenize and remove punctuation and lowercase 
        	tweet_content = [word.translate(table).lower() for word in tweet_content.split()] 
        
        	# remove non-alphanumeric and short words and filter out stop words
        	stop_words = set(stopwords.words('german'))
        	tweet_content = [word for word in tweet_content if word.isalpha() and len(word) > 2 and word not in stop_words]                
        
        	tokens_user += tweet_content
        
        	if index == 99:  # 100 tweets per user
        	    break
    
    except TwitterSearchException as e:  # take care of errors
        print(e, username)
        
    return tokens_user  #  list containing user's tokens


def save_tokens(filename, tokens_several_users):
    with open(filename, 'w') as f:
        for usertokens in tokens_several_users:
            f.write("%s\n" % ' '.join(usertokens))


def get_and_save_users_list(filename, list_of_usernames, my_consumer_key = keyfile.consumer_key, 
                            my_consumer_secret = keyfile.consumer_secret, 
                            my_access_token = keyfile.access_token, my_access_token_secret = keyfile.access_token_secret):
    tokens = mainsearch(usernames, my_consumer_key, my_consumer_secret, my_access_token, my_access_token_secret)
    tokens = [token for token in tokens if token != []]
    save_tokens(filename, tokens)
