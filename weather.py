# !/usr/bin/env python
#  -*- coding: utf-8 -*-
import json
import urllib2
from time import gmtime, strftime

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
	
	weather_dict['day'] = day
	weather_dict['time'] = time

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

	# print weather_data
	storeWeatherData(weather_data,town)

	# print "Current temperature in %s is: %s" % (location, temp_f)

	f.close() 

def removeAccentCharacters(string):
	""" Function that converts unicode characters to their ascii equivalent """
	if " " in string:
		string = string.replace(" ","%20") 
	# if u"á" in string:
	# 	string = string.replace("á","a")
	# if u"é" in string:
	# 	string = string.replace("é","e")
	# if u"í" in string:
	# 	string = string.replace("í","i")
	# if u"ó" in string:
	# 	string = string.replace("ó","o")
	# if u"ü" or u"ú" in string:
	# 	string = string.replace("ü","u")
	# 	string = string.replace("ú","u")
	return string

def storeWeatherData(weather_data,town):
	f = open('data/weather_'+town+'.json', 'a+')
	f.write(weather_data)
	f.write("\n")
# for tweet in tweets:
# # Verifying if tweet is not already in the dataset.
# if str(tweet) not in f.read():
## Store tweet, if not in dataset
# f.write(str(tweet) + "\n\n")
# # If tweet is in dataset, continue to the next iteration
# else:
# continue
	f.close()

if __name__ == '__main__':
	important_towns = ["San Juan","Ponce","Cabo Rojo","Mayaguez","Bayamon","Caguas","Fajardo","Humacao","Aguadilla","Carolina"]
	for town in important_towns:
		getWeatherFromWUnderground(town)

	print "Stored weather data on " + strftime("%Y-%m-%d %H:%M:%S", gmtime())