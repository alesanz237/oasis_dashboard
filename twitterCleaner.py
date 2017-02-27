#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys

#Reading Tweets

def retrieveTweets(file):
	""" Reading tweets file, cleaning tweets and storing them in a new file """
	tweets_data = []
	tweet = {}
	tweets_file = open(file, "r")
	for line in tweets_file:
		# print line
		try:
			tweets = json.loads(line)
			tweet["id"] = tweets["user"]["id"]
			tweet["created_at"] = tweets["created_at"]
			tweet["text"] = tweets["text"]
			tweet["location"] = tweets["user"]["location"]
			# print tweet
			tweets_data.append(tweet)
			tweet = {}
		except:
			continue
	return tweets_data
		
def getPositiveTweets():
	classified_sentences = []
	try:
		with open("data/tweets/positive.txt") as f:
			# classified_sentence = ()
			content = f.readlines()
			# print content
			for data in content:
				tweet = eval(data)
				sentence = tweet['text']
				polarity    = tweet['polarity']
				classified_sentence = (sentence,polarity)
				classified_sentences.append(classified_sentence)
	except:
		pass
	finally:
		with open("data/tweets/positive_backup.txt") as f:
			# classified_sentence = ()
			content = f.readlines()
			for data in content:
				tweet = eval(data)
				sentence = tweet['text']
				polarity    = tweet['polarity']
				classified_sentence = (sentence,polarity)
				classified_sentences.append(classified_sentence)
	return classified_sentences

def getNegativeTweets():
	classified_sentences = []
	try:
		with open("data/tweets/negative.txt") as f:
			# classified_sentence = ()
			content = f.readlines()
			# print content
			for data in content:
				tweet = eval(data)
				sentence = tweet['text']
				polarity    = tweet['polarity']
				classified_sentence = (sentence,polarity)
				classified_sentences.append(classified_sentence)
	except:
		pass
	finally:
		with open("data/tweets/negative_backup.txt") as f:
			# classified_sentence = ()
			content = f.readlines()
			for data in content:
				tweet = eval(data)
				sentence = tweet['text']
				polarity    = tweet['polarity']
				classified_sentence = (sentence,polarity)
				classified_sentences.append(classified_sentence)
	return classified_sentences

if __name__ == '__main__':
	print getPositiveTweets()