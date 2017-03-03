#!/usr/bin/env python
# -*- coding: utf-8 -*-

from params import lat_lon_towns
import json
from pprint import pprint
import time
import urllib2
import datetime
from config_twitter import api, place_id_towns, accounts
import csv
import sys  # Library needed for working with utf8 characters
reload(sys)  # Reseting system
sys.setdefaultencoding('utf8') # Setting the default encoding to utf8

def getLatLonByTown(town_name):
	""" Function that returns the coordinates of a town, given its name """
	int_coords = []
	for town in lat_lon_towns:
		if town_name == town:
			coordinates = lat_lon_towns[town_name].split(",",1)
	for coor in coordinates:
		int_coords.append(float(coor))
	print int_coords, "\n\n"
	return int_coords

def getWeatherFromOWM(town):
	""" Getting weather information by location from the Open Weather Map API """

	coors = getLatLonByTown(town) # Getting town coordinates

	# Getting weather data and storing it in a dictionary
	weather = owm.weather_at_coords(coors[0],coors[1]).get_weather()
	weather_data = {}
	weather_data["cloud_coverage"] = str(weather.get_clouds()) + "%" # Cloud Coverage
	weather_data["rain"]    	   = weather.get_rain()				   	   				  # Rain Volume
	weather_data["wind"] 		   = weather.get_wind()		   			   			  	  # Wind degree and speed
	weather_data["humidity"]  	   = str(weather.get_humidity()) + "%" 	  # Humidity percentage
	# weather_data["pressure"] 	   = weather.get_pressure()				   				  # Get Atmospheric pressure
	weather_data["temperature"]    = weather.get_temperature('fahrenheit') 				  # Get temperature
	weather_data["status"] 		   = weather.get_detailed_status()           # Get weather status

	# Parsing wind data
	speed = "" # String contianing the speed of the weather
	direction = "" # String containing the direction of the wind
	for key,value in weather_data["wind"].iteritems():
		if key == "speed":
			speed = str(value) +  " m/s"
		if key == "deg":
			if value == 0 or value == 360:
				direction = " north"
			elif value > 0 and value <= 90:
				direction = " northeast"
			elif value == 90:
				direction = " east"
			elif value > 90 and value <= 180:
				direction = " southeast"
			elif value == 180:
				direction = " south"
			elif value > 180 and value <= 270:
				direction = " southwest"
			elif value == 270:
				direction = " west"
			else:
				direction = " northwest"
	weather_data["wind"] = speed + direction

	# Parsing temperature data:
	weather_data["temperature"] = str(weather_data["temperature"]["temp"])

	# Parsing rain data
	weather_data["rain"] = str(weather_data["rain"]['3h']) if weather_data["rain"] else "No rain activy in the last three hours"

	return weather_data

def getWeatherFromNOAA(town):
	""" Getting weather information by location from NOAAA """

	coors = getLatLonByTown(town) # Getting town coordinates

	if coors == -1:
		return "ERROR: Could not get weather data"

	# Getting weather data and storing it in a json
	url = "http://forecast.weather.gov/MapClick.php?lat=" + str(coors[0]) + "&lon=" + str(coors[1]) + "&FcstType=json"
	# if town == "Aguadilla" or town == "Santa Isabel" or town == "Rincón" or town == "San Sebastián" or town == "Viewques":
		# url = "http://marine.weather.gov/MapClick.php?lat=" + str(coors[0]) + "&lon=" + str(coors[1]) + "&FcstType=json"
	print url
	data = json.load(urllib2.urlopen(url))
	weather_data = {} # Dictionary that will store the weather data
	# i = 0 # Counter value for dictionary
	for key,value in data.iteritems():
		i = 0 # Counter value for dictionary
		if key == "time":
			for period in value["startPeriodName"]:
				# Adding the day of the forecast to the weather data
				weather_data[i] = []
				weather_data[i].append(period)
				i +=1
			i = 0 # Reseting value of counter
			for label in value["tempLabel"]:
				# Adding the label of the forecast to the weather data
				weather_data[i].append(label)
				i +=1
		if key == "data":
			i = 0 # Reseting value of counter
			for temperature in value["temperature"]:
				weather_data[i].append(temperature)
				i +=1
			i = 0 # Reseting value of counter
			for weather in value["weather"]:
				weather_data[i].append(weather)
				i +=1	
			i = 0 # Reseting value of counter
			for icon in value["iconLink"]:
				weather_data[i].append(icon)
				i +=1
			i = 0 # Reseting value of counter
			for text in value["text"]:
				weather_data[i].append(text)
				i +=1		
		if key == "currentobservation":
			# print value
			current_observation = value
	# print weather_data

	return weather_data , current_observation

def getPlaceidByTown(town_name):
	""" Function that returns the place id of a town, given its name """
	place_id = ""
	for town in place_id_towns:
		if town_name == town:
			place_id = place_id_towns[town]
	return place_id

def getPRTweets(town):
    """ Funtion that gathers tweets from Puerto Rico"""
    pr_tweets = {}  # For storing tweets
    # final_tweet = {}
    # f = open('data/tweets.txt', 'a+')
    place_id = getPlaceidByTown(town)
    # Searching for tweets by municipality
    tweets = api.search(q="place:%s" % place_id)
    for tweet in tweets:
    	id_ = tweet.id
        text = tweet.text
        text = text.replace("\"","")
        text = text.replace("\n"," ")
        # final_tweet[tweet.id] = town + " | " + str(tweet.created_at) + " | " + tweet.text 
        json_string = "{\"coordinates\": \"" +  str(tweet.coordinates) + "\", \"created_at\": \"" + str(tweet.created_at) + "\", \"text\": \"" + text + "\"}" 
        # print json_string
        # array_of_tweets.append(json_string)
        pr_tweets[id_] = json_string
    # print pr_tweets
    # for tweet in array_of_tweets:
        # f.write(str(tweet) + "\n")
    # f.close()
    return pr_tweets

def getWeatherFromWUnderground(town):

	# Replacing unicode characters to their ascii equivalent
	
	town = removeAccentCharacters(town)

	url = "http://api.wunderground.com/api/c726e5a807dbc183/conditions/q/PR/"+town+".json"
	f = urllib2.urlopen(url)
	json_string = f.read()

	parsed_json = json.loads(json_string)

	current_observation = parsed_json["current_observation"]

	# Storing weather information in a dictionary
	weather_dict = {}
	observation_time = current_observation['observation_time_rfc822']
	weather_dict['observation_time'] = observation_time

	# Parsing time
	date_time_info = observation_time.split()
	day = date_time_info[0] + date_time_info[1] + date_time_info[2] + date_time_info[3]
	time = date_time_info[4]
	
	# weather[]

	weather = current_observation['weather']
	weather_dict['weather'] = weather

	temperature_string = current_observation['temperature_string']
	weather_dict['temperature_string'] = temperature_string

	temp_f = current_observation['temp_f']
	weather_dict['temp_f'] = temp_f

	temp_c = current_observation['temp_c']
	weather_dict['temp_c'] = temp_c

	relative_humidity = current_observation['relative_humidity']
	weather_dict['relative_humidity'] = relative_humidity

	wind_string = current_observation['wind_string']
	weather_dict['wind_string'] = wind_string

	wind_mph = current_observation['wind_mph']
	weather_dict['wind_mph'] = wind_mph

	wind_gust_mph = current_observation['wind_gust_mph']
	weather_dict['wind_gust_mph'] = wind_gust_mph

	wind_kph = current_observation['wind_kph']
	weather_dict['wind_kph'] = wind_kph

	wind_gust_kph = current_observation['wind_gust_kph']
	weather_dict['wind_gust_kph'] = wind_gust_kph

	pressure_mb = current_observation['pressure_mb']
	weather_dict['pressure_mb'] = pressure_mb

	dewpoint_string = current_observation['dewpoint_string']
	weather_dict['dewpoint_string'] = dewpoint_string

	dewpoint_f = current_observation['dewpoint_f']
	weather_dict['dewpoint_f'] = dewpoint_f

	dewpoint_c = current_observation['dewpoint_c']
	weather_dict['dewpoint_c'] = dewpoint_c

	heat_index_string = current_observation['heat_index_string']
	weather_dict['heat_index_string'] = heat_index_string

	heat_index_f = current_observation['heat_index_f']
	weather_dict['heat_index_f'] = heat_index_f

	heat_index_c = current_observation['heat_index_c']
	weather_dict['heat_index_c'] = heat_index_c

	solarradiation = current_observation['solarradiation']
	weather_dict['solarradiation'] = solarradiation

	uv = current_observation['UV']
	weather_dict['uv'] = uv

	precip_1hr_in = current_observation['precip_1hr_in']
	weather_dict['precip_1hr_in'] = precip_1hr_in

	precip_today_in = current_observation['precip_today_in']
	weather_dict['precip_today_in'] = precip_today_in

	# print parsed_json

	weather_data = json.dumps(weather_dict)

	print weather_data

	# print "Current temperature in %s is: %s" % (location, temp_f)

	f.close()

def removeAccentCharacters(string):
	""" Function that converts unicode characters to their ascii equivalent """
	if " " in string:
		string = string.replace(" ","%20") 
	if u"á" in string:
		string = string.replace("á","a")
	if u"é" in string:
		string = string.replace("é","e")
	if u"í" in string:
		string = string.replace("í","i")
	if u"ó" in string:
		string = string.replace("ó","o")
	if u"ü" or u"ú" in string:
		string = string.replace("ü","u")
		string = string.replace("ú","u")
	return string

def getKey1():
	key_1 = []
	with open('./data/AEE_SerieHistorica_2015.json') as data_file:
		energy_data = json.load(data_file)
	for dataset in energy_data:
		key_1.append(dataset)
	return key_1

def getKey2(key_1):
	key_2 = []
	with open('./data/AEE_SerieHistorica_2015.json') as data_file:
		energy_data = json.load(data_file)
	for dataset in energy_data[key_1]:
		key_2.append(dataset)
	return key_2

def getAEEData(key_1):
	fiscal_year = []
	final_result = []
	values = []
	result = {}
	suma = 0
	with open('./data/AEE_SerieHistorica_2015.json') as data_file:
		energy_data = json.load(data_file)
	for key_2 in energy_data[key_1]:
		for year in energy_data[key_1][key_2]:
			for month in energy_data[key_1][key_2][year]:
				suma +=energy_data[key_1][key_2][year][month]
			# print year, suma/12
			fiscal_year.append(year)
			fiscal_year.append(suma/12)
			values.append(fiscal_year)
			fiscal_year = []
			suma = 0
		result["key"] = key_2
		result["values"] = sorted(values)
		values = []
		final_result.append(result)
		result = {}
		# print final_resultx
	return final_result
		
def getMarketHistory(symbol, data_type, date):
	# data_type can be daily, monthly & yearly
	# print "Hello from getMarketHistory"
	day = date.split("-")[2]
	month = date.split("-")[1]
	year = str(int(date.split("-")[0])-1)
	new_date = year+month+day
	# print new_date
	final_result=[]
	results = {}
	results["values"] = []
	result = {}
	url = "http://marketdata.websol.barchart.com/getHistory.json?key=bb5776fcd3e1dd3c4ad7b7d691a0e83e&symbol=" 
	url += symbol
	url += "&type="
	url += data_type
	url += "&startDate="
	url += new_date
	# print url
	market_data = json.load(urllib2.urlopen(url))
	for data in market_data["results"]:
		result["open"]   = data["open"]
		result["high"]   = data["high"]
		result["low"]    = data["low"]
		result["close"]  = data["close"]
		result["volume"] = data["volume"]
		year 			 = int(data["tradingDay"].split("-")[0])
		month 			 = int(data["tradingDay"].split("-")[1])
		day 			 = int(data["tradingDay"].split("-")[2])
		date 			 = int(datetime.date(year,month,day).strftime("%s")) * 1000
		result["date"]	 = date
		results["values"].append(result)
		result = {}
	final_result.append(results)
	return final_result

def getStockSymbols():
	symbols = {}
	symbols["PowerShares QQQ Trust, Series 1"] = "QQQ"
	symbols["Facebook, Inc."] = "FB"
	# symbols["Apple Inc."] = "APPL"
	symbols["Netflix, Inc."] = "NFLX"
	symbols["Alphabet Inc Class A"] = "GOOGL"
	return symbols

def getMultipleSymbolHistory(symbols, data_type, date):
	final_result = []
	market_json = {}
	value = []
	values = []
	for symbol in symbols:
		market_json["key"] = symbol
		market_history = getMarketHistory(symbol, data_type, date)[0]["values"]
		# print market_history
		for i in range(0,len(market_history)):
			# pprint(market_history[i])
			value.append(market_history[i]["date"])
			value.append(market_history[i]["close"])
			values.append(value)
			value = []
		market_json["values"] = values
		values = []
		final_result.append(market_json)
		market_json = {}
	return final_result



# pprint(getMultipleSymbolHistory(["QQQ","FB","NFLX","GOOGL"],"daily","2016-11-14"))

