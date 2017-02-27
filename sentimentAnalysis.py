#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nltk
from generateTrainingSet import getTrainingSet
from twitterCleaner import retrieveTweets, getPositiveTweets, getNegativeTweets
import random
import csv
import time


energy_words = ["absorb","AC","accumulator","alternating current","anthracite coal","appliance","battery","biodiesel","biofuel","biomass","bituminous coal","blackout","boiler","British thermal unit","Btu","capacity","carbon","carbon footprint","carbon tax","charcoal","chemical energy","clean energy","climate change","coal","coke","combustion","conservation","crude oil","current","dam","DC","diesel","direct current","drill","dynamo","efficiency","efficient","electric","electrical","electrical grid","electromagnetic energy","electron","energy","engine","engineer","entropy","environment","erg","ethanol","fossil fuel","flexible fuel","flywheel","fuel","fuel cell","furnace","gas","gasoline","gas-turbine","generate","generation","generator","geothermal","global warming","green","green energy","greenhouse effect","greenhouse gas","grid","heat","heat exchange","high-voltage","horsepower","human-powered","hybrid","hydrocarbon","hydroelectric","hydrogen","hydrothermal","industry","internal combustion engine","inverter","jet fuel","joule","Kelvin scale","kilowatt","kilowatt-hour","kinetic energy","light","liquefied petroleum gas","magnetic energy","megawatt","methane","methanol","mining","motor","natural gas","nuclear","nuclear energy","nuclear power","nuclear reactor","nucleus","off-the-grid","oil","oil rig","peak oil","peat","petroleum","photon","photovoltaic","photovoltaic panel","pollution","potential energy","power","power grid","power lines","power plant","power station","power transmission","propane","public utility","radiant","radiate","reactor","reciprocating engine","reflect","renewable","reservoir","shale","solar panel","solar power","static electricity","steam","steam engine","steam turbine","sun","sunlight","sunshine","sustainable","temperature","therm","thermal energy","thermodynamics","tidal power","transmission lines","transmit","turbine","utilities","volt","waste","watt","wattage","wave power","wind","wind farm","windmill","wind power","wind turbine","work","absorber","acumulador","corriente alterna",u"carbón","aparato",u"batería","Biodiesel","Biocombustible","Biomasa",u"carbón bituminoso",u"apagón","caldera",u"Unidad Térmica Británica","BTU","capacidad",u"carbón","Huella de carbono","impuesto sobre el carbono",u"carbón",u"energía química",u"energia limpia",u"energía",u"cambio climático",u"carbón","coca",u"combustión",u"conservación",u"petróleo crudo","corriente","presa","corriente continua","diesel","corriente continua","perforar","dinamo","eficiencia","eficiente",u"eléctrico",u"eléctrico",u"red eléctrica",u"energía electromagnética",u"electrón",u"energía","motor","ingeniero",u"Entropía","ambiente","ergio","etanol","combustible fosil","Combustible flexible","volante","gasolina","pila de combustible","horno","gas","gasolina","turbina de gas","generar","Generacion","generador",u"Geotérmica","calentamiento global","verde",u"energía verde","efecto invernadero","gases de efecto invernadero",u"cuadrícula","calor","de intercambio de calor","Alto voltaje","caballo de fuerza"]
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
	# for tweet 
	for i in range(1,11):
		all_tweets = retrieveTweets("data/tweets/"+str(i)+".txt")
		for tweet in all_tweets:
			sentence = tweet["text"]
			created_at 	 = tweet["created_at"]
			try:
				polarity = classifier.classify(extract_features(sentence.split()))
				if polarity == "positive":
					f = open('data/tweets/positive.txt', 'a')
				else:
					f = open('data/tweets/negative.txt', 'a')
				stored_tweets["text"] = tweet["text"]
				stored_tweets["polarity"] = polarity
				stored_tweets["created_at"] = created_at
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
	try:
		with open('data/tweets/positive.txt') as f:
			for i, l in enumerate(f):
				pass
		positive_tweets = i + 1

		with open('data/tweets/negative.txt') as f:
			for i, l in enumerate(f):
				pass
		negative_tweets = i + 1
	except:
		pass
	finally:
		with open('data/tweets/positive_backup.txt') as f:
			for i, l in enumerate(f):
				pass
		positive_tweets = i + 1

		with open('data/tweets/negative_backup.txt') as f:
			for i, l in enumerate(f):
				pass
		negative_tweets = i + 1
	tweets_len = []
	tweets_len.append(positive_tweets)
	tweets_len.append(negative_tweets)
	return tweets_len

def getTweets():
	tweets = []
	try:
		with open('data/tweets/positive.txt') as tweet:
			for t in tweet:
				tweets.append(eval(t))
		with open('data/tweets/negative.txt') as tweet:
			for t in tweet:
				tweets.append(eval(t))
	except:
		pass
	finally:
		with open('data/tweets/positive_backup.txt') as tweet:
			for t in tweet:
				tweets.append(eval(t))
		with open('data/tweets/negative_backup.txt') as tweet:
			for t in tweet:
				tweets.append(eval(t))
	tweets = scrambled(tweets)
	return tweets

def getPositiveTweetsFromTo(_from,to):
	""" Getting positive tweets from a given time frame"""
	tweets = []
	tweet_dict = {}
	try:
		tweets = getTweetsFromRange('data/tweets/positive.txt',_from,to)
	except:
		pass
	finally:
		tweets = getTweetsFromRange('data/tweets/positive_backup.txt',_from,to)
	return tweets

def getTweetsFromRange(filename,_from,to):
	tweets = []
	tweet_dict = {}
	with open(filename) as tweet:
			for t in tweet:
				t = eval(t)
				date  = t['created_at'].split(" ")
				day   = date[2]
				month = date[1]
				if month == "Jan":
					month = "01"
				elif month == "Feb":
					month = "02"
				elif month == "Mar":
					month = "03"
				elif month == "Apr":
					month = "04"
				elif month == "May":
					month = "05"
				elif month == "Jun":
					month = "06"
				elif month == "Jul":
					month = "07"
				elif month == "Aug":
					month = "08"
				elif month == "Sep":
					month = "09"
				elif month == "Oct":
					month = "10"
				elif month == "Nov":
					month = "11"
				elif month == "Dec":
					month = 12
				hour  = date[3].split(":")[0]
				year  = date[5]
				date_time = day+"."+month+"."+year+" "+hour+":00"
				pattern = '%d.%m.%Y %H:%M'
				epoch = int(time.mktime(time.strptime(date_time, pattern)))
				# Getting how much hours do I have to store for array
				hours = to - _from
				hours_array = []
				updated_from = _from
				tweet_dict['x'] = epoch
				tweet_dict['y'] = 0
				print 'hours',hours
				for i in range(0,hours):
					if int(hour) == updated_from:
						tweet_dict['y'] += 1
						print tweet_dict
					if int(hour) > _from:
						tweets.append(tweet_dict)
						tweet_dict = {}
						hour +=1
					updated_from+=1	
	return tweets

def getNegativeTweetsFromTo(_from,to):
	""" Getting negative tweets from a given time frame"""
	tweets = []
	try:
		with open('data/tweets/negative.txt') as tweet:
			for t in tweet:
				t = eval(t)
				date  = t['created_at'].split(" ")
				day   = int(date[2])
				month = date[1]
				hour  = int(date[3].split(":")[0])
				year  = int(date[5])
				if hour >= _from and hour <= to:
					tweets.append(t)
	except:
		pass
	finally:
		with open('data/tweets/negative_backup.txt') as tweet:
			for t in tweet:
				t = eval(t)
				date  = t['created_at'].split(" ")
				day   = int(date[2])
				month = date[1]
				hour  = int(date[3].split(":")[0])
				year  = int(date[5])
				if hour >= _from and hour <= to:
					tweets.append(t)
	return tweets

def convertTweetsToCSV():
	""" Getting tweets from a given time frame"""
	# Gathering positive and negative tweets
	tweets = []
	try:
		with open('data/tweets/positive.txt') as tweet:
			for t in tweet:
				t = eval(t)
				tweets.append(t)
		with open('data/tweets/negative.txt') as tweet:
			for t in tweet:
				t = eval(t)
				tweets.append(t)
	except:
		pass
	finally:
		with open('data/tweets/positive_backup.txt') as tweet:
			for t in tweet:
				t = eval(t)
				tweets.append(t)
		with open('data/tweets/negative_backup.txt') as tweet:
			for t in tweet:
				t = eval(t)
				tweets.append(t)

	# Converting positive and negative tweets to csv
	date = time.strftime("%d-%m-%Y")
	filename = "data/tweets/tweets_"+date+".csv"
	f = csv.writer(open(filename, "wb+"))
	f.writerow(["created_at", "text", "polarity"])
	for tweet in tweets:
		try:
			f.writerow([tweet['created_at'],tweet['text'],tweet['polarity']])
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
	# print getCSVTweets("data/tweets/tweets_26-02-2017.csv")
	# storeClassifiedTweets()
	# print convertTweetsToCSV()
	print getPositiveTweetsFromTo(12,13)
	