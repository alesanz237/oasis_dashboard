# !/usr/bin/env python
#  -*- coding: utf-8 -*-
from forecastiopy import *
from params import lat_lon_towns, town_zipcodes, darksky
from unidecode import unidecode
from pprint import pprint
import datetime
import time
import csv

def getLatLonByTown(town_name):
	""" Function that returns the coordinates of a town, given its name """
	int_coords = []
	
	for town in lat_lon_towns:
		if town_name == town:
			coordinates = lat_lon_towns[town_name].split(",",1)
			break
		else:
			coordinates = []
		# elif town_name.lower() == town.lower():
		# 	coordinates = 
	for coor in coordinates:
		int_coords.append(float(coor))
	int_coords.append(getCorrectTownName(town_name))
	# print int_coords, "\n\n"
	# print len(int_coords)
	return int_coords if len(int_coords) > 1 else "ERROR: Invalid input given!"

def convertZipcodeToTown(zipcode):
	""" Function that returns the the name of a town, given its zipcode """
	for t_zipcode in town_zipcodes:
		if zipcode == t_zipcode:
			return town_zipcodes[t_zipcode]
	return None

def getCoords(keyword):
	""" Function that returns latitude and longitude for a given town or zipcode """
	keyword = unidecode(keyword.lower())
	if len(keyword) == 5 and keyword[0] == "0" and keyword[1] == "0":
		town = convertZipcodeToTown(keyword)
	else:
		town = keyword
	return getLatLonByTown(town)

def convertWindBearing(wind_bearing):
	""" Function that takes a int representation of wind_bearing and returns a string representation """
	wind_bearing = int(wind_bearing)
	bearing = ""
	if wind_bearing >= 0 and wind_bearing < 22.5:
		bearing = "N"
	if wind_bearing >= 22.5 and wind_bearing < 45:
		bearing = "NNE"
	if wind_bearing >= 45 and wind_bearing < 67.5:
		bearing = "NE"
	if wind_bearing >= 67.5 and wind_bearing < 90:
		bearing = "ENE"
	if wind_bearing >= 90 and wind_bearing < 112.5:
		bearing = "E"
	if wind_bearing >= 112.5 and wind_bearing < 135:
		bearing = "ESE"
	if wind_bearing >= 135 and wind_bearing < 157.5:
		bearing = "SE"
	if wind_bearing >= 157.5 and wind_bearing < 180:
		bearing = "S"
	if wind_bearing >= 180 and wind_bearing < 202.5:
		bearing = "SSW"
	if wind_bearing >= 202.5 and wind_bearing < 225:
		bearing = "SW"
	if wind_bearing >= 225 and wind_bearing < 247.5:
		bearing = "WSW"
	if wind_bearing >= 247.5 and wind_bearing < 270:
		bearing = "W"
	if wind_bearing >= 270 and wind_bearing < 292.5:
		bearing = "WNW"
	if wind_bearing >= 292.5 and wind_bearing < 315:
		bearing = "NW"
	if wind_bearing >= 315 and wind_bearing < 337.5:
		bearing = "NWN"
	if wind_bearing >= 337.5 and wind_bearing < 157.5:
		bearing = "N"
	return bearing

def getHourlyWeather(keyword, temp):
	"""Getting hourly data for location """
	coords = getCoords(keyword)
	conditions = []
	weather = {}
	if not isinstance(coords,str):
		if temp == "c":
			fio = ForecastIO.ForecastIO(darksky,
		                            units=ForecastIO.ForecastIO.UNITS_SI,
		                            lang=ForecastIO.ForecastIO.LANG_ENGLISH,
		                            latitude=coords[0], longitude=coords[1])
		else:
			fio = ForecastIO.ForecastIO(darksky,
		                            lang=ForecastIO.ForecastIO.LANG_ENGLISH,
		                            latitude=coords[0], longitude=coords[1])
		if fio.has_hourly() is True:
			hourly = FIOHourly.FIOHourly(fio)
			for hour in xrange(1, 13):
				for item in hourly.get_hour(hour).keys():
					if item == "icon":
						weather[item] = unicode(hourly.get_hour(hour)[item])
					if item == "summary":
						weather[item] = unicode(hourly.get_hour(hour)[item])
					if item == "temperature":
						if temp == "f":
							weather[item] = str(hourly.get_hour(hour)[item]).split(".")[0] + "° F"
						else:
							weather[item] = str(hourly.get_hour(hour)[item]).split(".")[0] + "° C"
					if item == "humidity":
						weather[item] = str(hourly.get_hour(hour)[item] * 100).split(".")[0] + "%"
					if item == "time":
						time = hourly.get_hour(hour)[item] 
						hours = datetime.datetime.fromtimestamp(time).strftime('%H:%M')
						date = datetime.datetime.fromtimestamp(time).strftime('%a %d, %b %Y')
						hour = int(hours.split(":")[0])
						minutes = hours.split(":")[1]
						if hour % 24 > 11:
							pm_or_am = " PM"
						else:
							pm_or_am = " AM"
						modded_hour = hour % 12
						if modded_hour == 0:
							modded_hour = 12
						weather[item] = date + " " + str(modded_hour) + ":" + minutes + pm_or_am
					if item == "precipProbability":
						weather[item] = str(hourly.get_hour(hour)[item] * 100).split(".")[0] + "%"
					if item == "windSpeed":
						windSpeed = unicode(hourly.get_hour(hour)[item])
					if item == "windBearing":
						windBearing = unicode(hourly.get_hour(hour)[item])
						windBearing = convertWindBearing(windBearing)
						weather["wind"] = windBearing + " " + windSpeed + " mph"
				conditions.append(weather)
				weather = {}
		else:
			return 'No Hourly data'
	else:
		return coords
	return conditions

def getHourlyWeatherInCSV(keyword, temp):
	coords = getCoords(keyword)
	conditions = []
	weather = {}
	if not isinstance(coords,str):
		if temp == "c":
			fio = ForecastIO.ForecastIO(darksky,
		                            units=ForecastIO.ForecastIO.UNITS_SI,
		                            lang=ForecastIO.ForecastIO.LANG_ENGLISH,
		                            latitude=coords[0], longitude=coords[1])
		else:
			fio = ForecastIO.ForecastIO(darksky,
		                            lang=ForecastIO.ForecastIO.LANG_ENGLISH,
		                            latitude=coords[0], longitude=coords[1])
		if fio.has_hourly() is True:
			hourly = FIOHourly.FIOHourly(fio)
			for hour in xrange(0, 24):
				for item in hourly.get_hour(hour).keys():
					if item == "icon":
						weather[item] = unicode(hourly.get_hour(hour)[item])
					if item == "summary":
						weather[item] = unicode(hourly.get_hour(hour)[item])
					if item == "temperature":
						if temp == "f":
							weather[item] = str(hourly.get_hour(hour)[item]).split(".")[0] + " F"
						else:
							weather[item] = str(hourly.get_hour(hour)[item]).split(".")[0] + " C"
					if item == "humidity":
						weather[item] = str(hourly.get_hour(hour)[item] * 100).split(".")[0] + "%"
					if item == "time":
						time = hourly.get_hour(hour)[item] 
						hours = datetime.datetime.fromtimestamp(time).strftime('%H:%M')
						date = datetime.datetime.fromtimestamp(time).strftime('%a %d, %b %Y')
						hour = int(hours.split(":")[0])
						minutes = hours.split(":")[1]
						if hour % 24 > 11:
							pm_or_am = " PM"
						else:
							pm_or_am = " AM"
						modded_hour = hour % 12
						if modded_hour == 0:
							modded_hour = 12
						weather[item] = date + " " + str(modded_hour) + ":" + minutes + pm_or_am
					if item == "precipProbability":
						weather[item] = str(hourly.get_hour(hour)[item] * 100).split(".")[0] + "%"
					if item == "windSpeed":
						windSpeed = unicode(hourly.get_hour(hour)[item])
					if item == "windBearing":
						windBearing = unicode(hourly.get_hour(hour)[item])
						windBearing = convertWindBearing(windBearing)
						weather["wind"] = windBearing + " " + windSpeed + " mph"
				conditions.append(weather)
				weather = {}
		else:
			return 'No Hourly data'
	else:
		return coords
	if keyword[0] == "0":
		keyword = convertZipcodeToTown(keyword)
	keyword = getCorrectTownName(keyword)
	if temp == 'f':
		filename = "data/weather/"+keyword+"_f.csv"
	else:
		filename = "data/weather/"+keyword+"_c.csv"
	f = csv.writer(open(filename, "wb+"))
	f.writerow(["date", "description", "precipitation", "temperature", "humidity", "wind", "icon"])
	for condition in conditions:
		try:
			f.writerow([condition['time'],
				condition['summary'],
				condition['precipProbability'],
				condition['temperature'],
				condition['humidity'],
				condition['wind'],
				condition['icon']])
		except:
			pass

def getTodaysWeather(keyword, temp):
	""" Function that returns today's weather given a towns name or zipcode """
	coords = getCoords(keyword)
	weather = {}
	if not isinstance(coords,str):
		if temp == "c":
			fio = ForecastIO.ForecastIO(darksky,
		                            units=ForecastIO.ForecastIO.UNITS_SI,
		                            lang=ForecastIO.ForecastIO.LANG_ENGLISH,
		                            latitude=coords[0], longitude=coords[1])
		else:
			fio = ForecastIO.ForecastIO(darksky,
		                            lang=ForecastIO.ForecastIO.LANG_ENGLISH,
		                            latitude=coords[0], longitude=coords[1])
		if fio.has_daily() is True and fio.has_hourly() is True:
		    daily = FIODaily.FIODaily(fio)
		    hourly = FIOHourly.FIOHourly(fio)
		    for day in xrange(0, 1):
				for item in daily.get_day(day).keys():
					if item == "temperatureMin":
						weather[item] = str(daily.get_day(day)[item]).split(".")[0]
					if item == "summary":
						weather[item] = unicode(daily.get_day(day)[item])
					if item == "temperatureMax":
						weather[item] = str(daily.get_day(day)[item]).split(".")[0]
					if item == "windSpeed":
						windSpeed = unicode(daily.get_day(day)[item])
					if item == "windBearing":
						windBearing = unicode(daily.get_day(day)[item])
						windBearing = convertWindBearing(windBearing)
					if item == "sunsetTime":
						sunsetTime = daily.get_day(day)[item] 
						sunsetTime = datetime.datetime.fromtimestamp(sunsetTime).strftime('%H:%M')
						hour = int(sunsetTime.split(":")[0])
						minutes = sunsetTime.split(":")[1]
						if hour % 24 > 11:
							pm_or_am = " PM"
						else:
							pm_or_am = " AM"
						modded_hour = hour % 12
						if modded_hour == 0:
							modded_hour = 12
						weather[item] = str(modded_hour) + ":" + minutes + pm_or_am
					if item == "sunriseTime":
						sunriseTime = daily.get_day(day)[item] 
						sunriseTime = datetime.datetime.fromtimestamp(sunriseTime).strftime('%H:%M')
						hour = int(sunriseTime.split(":")[0])
						minutes = sunriseTime.split(":")[1]
						if hour % 24 > 11:
							pm_or_am = " PM"
						else:
							pm_or_am = " AM"
						modded_hour = hour % 12 
						if modded_hour == 0:
							modded_hour = 12
						weather[item] = str(modded_hour) + ":" + minutes + pm_or_am
					if item == "precipProbability":
						weather[item] = str(hourly.get_hour(hour)[item] * 100).split(".")[0] + "%"
				weather["wind"] = windBearing + " " + windSpeed + " mph"
				for item in hourly.get_hour(day).keys():
					if item == "summary":
						weather["current"] = unicode(hourly.get_hour(0)[item])
					if item == "temperature":
						weather[item] = str(hourly.get_hour(0)[item]).split(".")[0]
					if item == "icon":
						weather[item] = unicode(hourly.get_hour(0)[item])
				weather["town"] = coords[2]

		else:
		    return 'No Todays data'
	else:
		return coords
	return weather

def getDailyWeather(keyword, temp):
	# Getting daily data for location (7 days )
	coords = getCoords(keyword)
	daily_weather = []
	weather = {}
	if not isinstance(coords,str):
		if temp == "c":
			fio = ForecastIO.ForecastIO(darksky,
		                            units=ForecastIO.ForecastIO.UNITS_SI,
		                            lang=ForecastIO.ForecastIO.LANG_ENGLISH,
		                            latitude=coords[0], longitude=coords[1])
		else:
			fio = ForecastIO.ForecastIO(darksky,
		                            lang=ForecastIO.ForecastIO.LANG_ENGLISH,
		                            latitude=coords[0], longitude=coords[1])
		if fio.has_daily() is True:
			daily = FIODaily.FIODaily(fio)
			for day in xrange(0, 4):
				for item in daily.get_day(day).keys():
					if item == "summary":
						weather[item] = unicode(daily.get_day(day)[item])
					if item == "icon":
						weather[item] = unicode(daily.get_day(day)[item])
					if item == "temperatureMax":
						weather[item] = str(daily.get_day(day)[item]).split(".")[0]	
					if item == "temperatureMin":
						weather[item] = str(daily.get_day(day)[item]).split(".")[0]
					if item == "precipProbability":
						weather[item] = str(daily.get_day(day)[item] * 100).split(".")[0] + "%"
					if item == "time":
						time = daily.get_day(day)[item] 
						hours = datetime.datetime.fromtimestamp(time).strftime('%H:%M')
						date = datetime.datetime.fromtimestamp(time).strftime('%a %d, %b %Y')
						hour = int(hours.split(":")[0])
						minutes = hours.split(":")[1]
						if hour % 24 > 11:
							pm_or_am = " PM"
						else:
							pm_or_am = " AM"
						modded_hour = hour % 12
						if modded_hour == 0:
							modded_hour = 12
						weather[item] = date 
				daily_weather.append(weather)
				weather = {}
		else:
			return 'No Daily data'
	else:
		return coords
	return daily_weather

def getCorrectTownName(town):
	if town == "anasco":
		town =  u"Añasco"
	elif town == "bayamon":
		town = u"Bayamón"
	elif town == "canovanas":
		town = u"Canóvanas"
	elif town == "catano":
		town = u"Cataño"
	elif town == "comerio":
		town = "Comerío"
	elif town == "guanica":
		town = "Guánica"
	elif town == "juana diaz":
		town = u"Juana Díaz"
	elif town == "las marias":
		town = u"Las Marías"
	elif town == "loiza":
		town = u"Loíza"
	elif town == "manati":
		town = u"Manatí"
	elif town == "mayaguez":
		town = u"Mayagüez"
	elif town == "penuelas":
		town = u"Peñuelas"
	elif town == "rincon":
		town = u"Ricón"
	elif town == "rio grande":
		town = "Río Grande"
	elif town == "san german":
		town = "San Germán"
	elif town == "san sebastian":
		town = "San Sebastián"
	else:
		town = town.title()
	return town 

def readWeatherInCSV(file):
	""" Function that reads data from a csv file and converts it to json """
	weather = []
	with open(file) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			attributes = {}
			attributes['date'] = row['date']
			attributes['description']		 = row['description']
			attributes['precipitation']   = row['precipitation']
			attributes['humidity'] = row['humidity']
			attributes['temperature']		 = row['temperature']
			attributes['wind']   = row['wind']
			attributes['icon']   = row['icon']
			weather.append(attributes)

	return weather

# def getWeatherAttributeForComparison(weather):


# if __name__ == '__main__':
	# getHourlyWeatherInCSV(u"00680","c")
	# print getTodaysWeather(u"cayey","f")
	# print getDailyWeather(u"00680","f")
	# pprint(getHourlyWeather(u"00680","f"))
	# pprint(readWeatherInCSV("data/weather/Mayagüez_f.csv"))