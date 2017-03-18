#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nltk
from generateTrainingSet import getTrainingSet
from twitterCleaner import retrieveTweets, getPositiveTweets, getNegativeTweets
from params import energy_words
import random
import csv
import time
import subprocess
#Example positive tweets
t_set = getTrainingSet() 

# Generating list of positive and negative tweets
tweets = []
for (words, sentiment) in t_set:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3] 
    tweets.append((words_filtered, sentiment))

"""
	The list of word features need to be extracted from the tweets. It is a list with every distinct words ordered by frequency of appearance. 
	We use the following function to get the list plus the two helper functions
"""
def get_words_in_tweets(tweets):
	""" Gives us the words for every tweet """
	all_words = []
	for (words, sentiment) in tweets:
		all_words.extend(words)
	return all_words

def get_word_features(wordlist):
	""" Determines the frequency for each word on a list """
	wordlist = nltk.FreqDist(wordlist)
	word_features = wordlist.keys()
	return word_features

def get_word_features_and_values(wordlist):
	""" Determines the frequency for each word on a list """
	word_features_and_values = {}
	wordlist = nltk.FreqDist(wordlist)
	word_features = wordlist.keys()
	word_values = wordlist.values()
	for i in range(0,len(word_features)):
		for word in energy_words:
			if word_features[i] == word:
				word_features_and_values[word_features[i]] = word_values[i]
	return list(reversed(sorted(word_features_and_values.items(), key=lambda x: x[1])))[0:10]


word_features = get_word_features(get_words_in_tweets(tweets))

# Extracting relevant features 
def extract_features(document):
	document_words = set(document)
	features = {}
	for word in word_features:
		features['contains(%s)' % word] = (word in document_words)
	return features

def storeClassifiedTweets():
	# Variable that contains the labeled datasets
	training_set = nltk.classify.apply_features(extract_features, tweets)
	# Training our classifier
	classifier = nltk.NaiveBayesClassifier.train(training_set)
	stored_tweets = {}
	# Classifying tweets 
	all_tweets = retrieveTweets("data/tweets/tweets.txt")
	for tweet in all_tweets:
		sentence    = tweet["text"]
		created_at 	= tweet["created_at"]
		location    = tweet["location"]
		try:
			polarity = classifier.classify(extract_features(sentence.split()))
			if "puerto rico" in location.lower():
				if polarity == "positive":
					f = open('data/tweets/positive.txt', 'a')
				else:
					f = open('data/tweets/negative.txt', 'a')	
				stored_tweets["text"]       = sentence
				stored_tweets["polarity"]   = polarity
				stored_tweets["created_at"] = created_at
				stored_tweets["location"]   = location
				f.write(str(stored_tweets))
				f.write("\n")
				f.close()
		except:
			continue

	convertTweetsToCSV()

def getPositiveWords():
	tweets = []
	for (words, sentiment) in getPositiveTweets() :
		words_filtered = [e.lower() for e in words.split() if len(e) >= 3] 
		tweets.append((words_filtered, sentiment))
	word_features_and_values =  get_word_features_and_values(get_words_in_tweets(tweets))
	word_values = {}
	labels_and_values = []
	for word_and_values in word_features_and_values:
		label = word_and_values[0]
		value = word_and_values[1]
		# print label,value
		word_values["label"] = label
		word_values["value"] = value
		labels_and_values.append(word_values)
		word_values = {}
	return labels_and_values

def getNegativeWords():
	tweets = []
	for (words, sentiment) in getNegativeTweets() :
		words_filtered = [e.lower() for e in words.split() if len(e) >= 3] 
		tweets.append((words_filtered, sentiment))
	word_features_and_values =  get_word_features_and_values(get_words_in_tweets(tweets))
	word_values = {}
	labels_and_values = []
	for word_and_values in word_features_and_values:
		label = word_and_values[0]
		value = word_and_values[1]
		# print label,value
		word_values["label"] = label
		word_values["value"] = value
		labels_and_values.append(word_values)
		word_values = {}
	return labels_and_values

def getTweetsLen():
	""" Method that returns how many tweets are available """

	with open('data/tweets/positive.txt') as f:
		for i, l in enumerate(f):
			pass
	positive_tweets = i + 1

	with open('data/tweets/negative.txt') as f:
		for i, l in enumerate(f):
			pass
		negative_tweets = i + 1
	tweets_len = []
	tweets_len.append(positive_tweets)
	tweets_len.append(negative_tweets)
	return tweets_len

def getTweets():
	tweets = []
	with open('data/tweets/positive.txt') as tweet:
		for t in tweet:
			tweets.append(eval(t))
	with open('data/tweets/negative.txt') as tweet:
		for t in tweet:
			tweets.append(eval(t))
	tweets = scrambled(tweets)
	return tweets

def getPositiveTweetsFromTo(_from,to):
	""" Getting positive tweets from a given time frame"""
	tweets = []
	tweet_dict = {}
	tweets = getTweetsFromRange('data/tweets/positive.txt',_from,to)
	return tweets

def getNegativeTweetsFromTo(_from,to):
	""" Getting negative tweets from a given time frame"""
	tweets = []
	tweet_dict = {}
	tweets = getTweetsFromRange('data/tweets/negative.txt',_from,to)
	return tweets

def getTweetsFromRange(filename,_from,to):
	tweets = []
	tweet_dict = {}
	dict_of_tweets = {}
	counter = 1
	tweet_dict['y'] = 0
	updated_from = _from
	with open(filename) as tweet:
		for t in tweet:
			t = eval(t)
			date  = t['created_at'].split(" ")
			day   = date[2]
			month = date[1]
			hour  = date[3].split(":")[0]
			year  = date[5]
			date_time = day+"."+month+"."+year+" "+hour+":00"
			hour = int(hour)
			pattern = '%d.%b.%Y %H:%M'
			epoch = int(time.mktime(time.strptime(date_time, pattern)))
			# Getting how much hours do I have to store for array
			hours = to - _from
			
			tweet_dict['x'] = epoch
			# print 'hours',hours
			
			for i in range(0,hours):
				dict_of_tweets[updated_from] = 0
				print 'updated_from',updated_from
				if hour == updated_from:
					dict_of_tweets[updated_from] += counter
					counter+=1
			# if hour > updated_from:
			# 	updated_from +=1
					# tweet_dict['y'] += 1
			# 		# print tweet_dict
			# 	updated_from 
			# print "hour",hour
			# if hour >= updated_from:
			# 	tweets.append(tweet_dict)
			# 	tweet_dict = {}
			# 	tweet_dict['y'] = 0
			# 	updated_from+=1	
	# print tweet_dict
	print dict_of_tweets
	return tweets

def convertTweetsToCSV():
	""" Getting tweets from a given time frame"""
	# Gathering positive and negative tweets
	subprocess.Popen('code/processes/deleteTwitterData.sh',shell=True)
	tweets = []
	with open('data/tweets/positive.txt') as tweet:
		for t in tweet:
			t = eval(t)
			tweets.append(t)
	with open('data/tweets/negative.txt') as tweet:
		for t in tweet:
			t = eval(t)
			tweets.append(t)

	# Converting positive and negative tweets to csv
	date = time.strftime("%d-%m-%Y")
	filename = "data/tweets/tweets.csv"
	f = csv.writer(open(filename, "wb+"))
	f.writerow(["created_at","location","text","polarity"])
	for tweet in tweets:
		try:
			f.writerow([tweet['created_at'],tweet['location'],tweet['text'],tweet['polarity']])
		except:
			pass

def getCSVTweets(file):
	""" Getting CSV tweets """
	# tweets = csv.reader("test.csv")
	tweets = []
	# for tweet in tweets:
		# print tweet
	with open(file) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			tweet = {}
			tweet['created_at'] = row['created_at']
			tweet['text']		 = row['text']
			tweet['polarity']   = row['polarity']
			tweets.append(tweet)

	return tweets

def scrambled(orig):
	""" Scrambles python list """
	dest = orig[:]
	random.shuffle(dest)
	return dest

if __name__ == '__main__':
	storeClassifiedTweets()


	