# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

import json
from params import positive_words, negative_words, energy_words

def getTweets():
    # f = open('data/tweets.txt', 'r')
    # data = '{"id":"727922684399489025", "coordinates": "None", "created_at": "2016-05-04 18:07:46", "text": "Llamado de @DavidBernierPR al gobernador en torno al B2B | \"El bolsillo no aguanta más\" - https://t.co/aZ9JItd9rE https://t.co/3qYYSWVwqE"}'
    # tweet = json.loads(data)
    # print tweet
    array_of_tweets = []
    with open('data/tweets.txt', 'r') as f:
        for line in f:
            # print line
            tweet = json.loads(line)
            array_of_tweets.append(tweet)
    #         break
    print "Total tweet count: ",len(array_of_tweets)
    return array_of_tweets

def getPositiveTweets(tweets):
    count = 0
    positive_word = []
    for tweet in tweets:
        for word in positive_words:
            if word in tweet["text"]:
                # positive_dict[word] += 1
                count+=1
                positive_word.append(word)
                # print tweet
    # for word in positive_word:
        # print word, positive_word.count(word)
    print "Positive word count: ",count

def getNegativeTweets(tweets):
    count = 0
    negative_word = []
    for tweet in tweets:
        for word in negative_words:
            if word in tweet["text"]:
                # positive_dict[word] += 1
                count+=1
                negative_word.append(word)
                # print tweet
    for word in negative_word:
        print word, negative_word.count(word)
    print "Negative word count: ",count

def getEnergyTweets(tweets):
    count = 0
    energy_tweets = []
    for tweet in tweets:
        for word in energy_words:
            if word in tweet["text"]:
                count+=1
                energy_tweets.append(tweet)
    print "Energy word count: ",count
    return energy_tweets

if __name__ == '__main__':
    tweets = getTweets()
    energy_tweets =getEnergyTweets(tweets)
    # print energy_words
    # print positive_words
    # print negative_words
    getPositiveTweets(energy_tweets)
    getNegativeTweets(energy_tweets)