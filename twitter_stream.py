# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
"""
    Programmer: Alejandro Sánchez
    Script that gathers tweets from the 78 municipalities of Puerto Rico 
    and stores it in a file.
"""
<<<<<<< HEAD
from config_twitter import api, place_id_towns, accounts
import json
import csv
import sys  # Library needed for working with utf8 characters
reload(sys)  # Reseting system
sys.setdefaultencoding('utf8') # Setting the default encoding to utf8

def getPRTweets():
    """ Funtion that gathers tweets from Puerto Rico"""
    array_of_tweets = []  # For storing tweets
    # final_tweet = {}
    f = open('data/tweets.txt', 'a+')
    for town, place_id in place_id_towns.iteritems():
        # Searching for tweets by municipality
        tweets = api.search(q="place:%s" % place_id)
        for tweet in tweets:
            text = tweet.text
            text = text.replace("\"","")
            text = text.replace("\n"," ")
            # final_tweet[tweet.id] = town + " | " + str(tweet.created_at) + " | " + tweet.text 
            json_string = "{\"id\":\"" + str(tweet.id) + "\", \"coordinates\": \"" +  str(tweet.coordinates) + "\", \"created_at\": \"" + str(tweet.created_at) + "\", \"text\": \"" + text + "\"}" 
            # print json_string
            array_of_tweets.append(json_string)
    for tweet in array_of_tweets:
        f.write(str(tweet) + "\n")
    f.close()
    # return array_of_tweets

def getUserTweets(username):
    """ Function that gathers tweets by username"""
    # print username
    array_of_tweets = []  # For storing tweets
    # final_tweet = {}
    tweets = api.user_timeline(screen_name = username,count=200, include_rts = True)
    f = open('data/tweets.txt', 'a+')
    for tweet in tweets:
            text = tweet.text
            text = text.replace("\"","")
            text = text.replace("\n"," ")
            json_string = "{\"id\":\"" + str(tweet.id) + "\", \"coordinates\": \"" +  str(tweet.coordinates) + "\", \"created_at\": \"" + str(tweet.created_at) + "\", \"text\": \"" + text + "\"}" 
            # print json_string
            array_of_tweets.append(json_string)
    # len_of_tweets = len(array_of_tweets) # Storing the length of the array of tweets for calculations
    for tweet in array_of_tweets:
        f.write(str(tweet) + "\n")
        # print tweet
    f.close()
    # return array_of_tweets
=======
from config_twitter import api, place_id_locations

def getTweets():
    """ Funtion that gathers tweets from Puerto Rico"""
    tweets = api.search(q="place:%s" % "624c7c7a6c0e0b6c")
    for place_id in place_id_locations:
        # Searching for tweets by municipality
        tweets = api.search(q="place:%s" % place_id)
    return tweets
>>>>>>> 722aaa28f47d80533133cc705ce5d48b32cc09d2

def storeTweets(tweets):
    """ Storing tweets in a file """
    # File where tweets will be stored
<<<<<<< HEAD
    f = open('data/new_tweets.txt', 'a+')
    for tweet in tweets:
        # Verifying if tweet is not already in the dataset.
        if str(tweet) not in f.read():
            # Store tweet, if not in dataset
            f.write(str(tweet) + "\n")
=======
    f = open('data/tweets.txt', 'a+')
    for tweet in tweets:
        # Verifying if tweet is not already in the dataset.
        if tweet and str(tweet.id) not in f.read():
            # Store tweet, if not in dataset
            f.write(str(tweet) + "\n\n")
>>>>>>> 722aaa28f47d80533133cc705ce5d48b32cc09d2
        # If tweet is in dataset, continue to the next iteration
        else:
            continue
    f.close()

<<<<<<< HEAD
def getPRTrends():
    """ Getting the current trends in Puerto Rico"""
    trends = [] # Empty array where trends will be stored. 
    results = api.trends_place(id= 23424935)
    for location in results:
        for trend in location["trends"]:
            trends.append(trend["name"])
            print trend
    return trends

def getTrendingTweets():
    """ Getting tweets by trends """
    trends = getPRTrends()
    final_tweet = {}
    array_of_tweets = [] # Empty array where trends will be stored.
    f = open('data/tweets.txt', 'a+')
    for trend in trends:
        trendingTweets = api.search(q=trend)
        for tweet in trendingTweets:
            text = tweet.text
            text = text.replace("\"","")
            text = text.replace("\n"," ")
            json_string = "{\"id\":\"" + str(tweet.id) + "\", \"coordinates\": \"" +  str(tweet.coordinates) + "\", \"created_at\": \"" + str(tweet.created_at) + "\", \"text\": \"" + text + "\"}"
            array_of_tweets.append(json_string)
        # storeTweets(trendingTweets)
    for tweet in array_of_tweets:
        f.write(str(tweet) + "\n")
        # print tweet
    f.close()
    # return array_of_tweets

def readTweets():
    # f = open('data/tweets.txt', 'r')
    # data = '{"id":"727922684399489025", "coordinates": "None", "created_at": "2016-05-04 18:07:46", "text": "Llamado de @DavidBernierPR al gobernador en torno al B2B | \"El bolsillo no aguanta más\" - https://t.co/aZ9JItd9rE https://t.co/3qYYSWVwqE"}'
    # tweet = json.loads(data)
    # print tweet
    array_of_tweets = []
    with open('data/new_tweets.txt', 'r') as f:
        for line in f:
            # print line
            tweet = json.loads(line)
            array_of_tweets.append(tweet)
    #         break
    for tweet in array_of_tweets:
        print tweet["text"]

if __name__ == '__main__':
    getPRTweets()
    getTrendingTweets()
    # Getting tweets
    # print "Getting tweets..."
    # readTweets()
    # prTweets = getPRTweets()
    # storeTweets(prTweets)
    # Getting tweets by username and storing them
    for username in accounts:
        userTweets = getUserTweets(username)
        # storeTweets(userTweets)
    # trendingTweets = getTrendingTweets()
    # storeTweets(trendingTweets)
    # Storing tweets
    # print "Storing tweets..."
    
    # print "Finished storing tweets."

    
=======
if __name__ == '__main__':
    # Getting tweets
    tweets = getTweets()
    # Storing tweets
    storeTweets(tweets)
>>>>>>> 722aaa28f47d80533133cc705ce5d48b32cc09d2
