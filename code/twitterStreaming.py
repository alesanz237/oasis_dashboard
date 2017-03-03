#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from params import energy_words, access_token, access_token_secret, consumer_key, consumer_secret

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

	def __init__(self):
		self.num_tweets = 0

	def on_data(self, data):
		# if (time.time() - self.start_time) < self.limit:
		if self.num_tweets < 10000:
			print data
			self.num_tweets+=1
			return True
		return False

	def on_error(self, status):
		print status			


if __name__ == '__main__':

	#This handles Twitter authetification and the connection to Twitter Streaming API
	l = StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	stream = Stream(auth, l)

	#This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
	stream.filter(track=energy_words)