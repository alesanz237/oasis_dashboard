# !/usr/bin/env python
#  -*- coding: utf-8 -*-
import time
import calendar
from params import lat_lon_towns, town_zipcodes, darksky
from unidecode import unidecode
from forecastiopy import *
from datetime import datetime

class Helper():
	"""
		Class that has functions used for computations in other classes
	"""
	# def __init__(self, arg):
	# 	self.day    = time.strftime("%d")
	# 	self.month  = time.strftime("%m")
	# 	self.year   = time.strftime("%Y")
	# 	self.hour   = time.strftime("%H")
	# 	self.minute = time.strftime("%M")
		
	def isEndOfMonth(self, month, day):
		""" 
			Function that determines if its the last day of the month

			Returns: 
				bool: True if its end of the month, False otherwise.
		"""

		return ((month == 1 and day == 31) or (month == 2 and day == 28)  or
				(month == 3 and day == 31) or (month == 4 and day == 30)  or
				(month == 5 and day == 31) or (month == 6 and day == 30)  or
				(month == 7 and day == 31) or (month == 8 and day == 31)  or
				(month == 9 and day == 30) or (month == 10 and day == 31) or
				(month == 11 and day == 30) or (month == 12 and day == 31))

	def getDay(self):
		""" Returns the current day """
		return time.strftime("%d")

	def getMonth(self):
		""" Returns the current month """
		return time.strftime("%m")

	def getYear(self):
		""" Returns the current year """
		return time.strftime("%Y")

	def getHour(self):
		""" Returns the current hour """
		return time.strftime("%H")

	def getYesterday(self):
		""" 
			Returns yesterday in an array.
			[year,month,day]
		"""
		yesterday = []
		current_day = int(self.getDay())-1
		current_year = int(self.getYear())
		current_month = self.getMonth()
		if current_day == 0:
			current_month = int(self.getMonth()) -1
			if (current_month == 1 or current_month == 3 or
				current_month == 5 or current_month == 7 or
				current_month == 8 or current_month == 10 or
				current_month == 12 or current_month == 12):
				current_day	= 31
			elif (current_month == 2):
				current_day = 28
			else:
				current_day = 30
			if current_month == 0:
				current_month = 31
				current_year = int(self.getYear()) - 1
			# yesterday = str(current_year)+str(current_month)
		if len(str(current_day)) == 1:
			current_day = "0" + str(current_day)
		yesterday.append(str(current_year))
		yesterday.append(str(current_month))
		yesterday.append(str(current_day))

		return yesterday

	def getDateInEpoch(self, timestamp):
		""" Returns the current time in epoch """
		if "/" in timestamp:
			return calendar.timegm(time.strptime(timestamp,'%m/%d/%Y %H:%M'))
		else:
			return calendar.timegm(time.strptime(timestamp,'%a %d, %b %Y %H:%M %p'))

	def getLatLonByTown(self, town_name):
		""" 
			Function that returns the coordinates of a town, given its name

			Returns: 
				array: Coordinates for a given town and town name. If town name invalid
				return mayaguez coordinates
		"""

		int_coords = []
		
		for town in lat_lon_towns:
			if town_name == town:
				coordinates = lat_lon_towns[town_name].split(",",1)
				break
			else:
				coordinates = []

		for coor in coordinates:
			int_coords.append(float(coor))
		int_coords.append(self.getCorrectTownName(town_name))

		return int_coords if len(int_coords) > 1 else [18.2019615, -67.1686406, u'Mayagüez']

	def convertZipcodeToTown(self, zipcode):
		""" 
			Function that returns the the name of a town, given its zipcode

			Returns: 
				String: Empty if no town name is found given zipcode, otherwise
				returns townname
		"""

		towname = ""

		for t_zipcode in town_zipcodes:
			if zipcode == t_zipcode:
				towname = town_zipcodes[t_zipcode]

		return towname

	def getCoords(self, keyword):
		""" 
			Function that returns latitude, longitude and town name 
			for a given town or zipcode

			Returns: 
				array: Coordinates for a given town and town name. If town name invalid
				return mayaguez coordinates
		"""

		keyword = unidecode(keyword.lower())

		if len(keyword) == 5 and keyword[0] == "0":
			keyword = self.convertZipcodeToTown(keyword)

		return self.getLatLonByTown(keyword)

	def convertWindBearing(self, wind_bearing):
		""" 
			Function that takes a int representation of wind_bearing and returns a string representation

			Returns: 
				String: wind representation
		"""

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

	def getCorrectTownName(self, town):
		""" 
			Function that returns the correct town name 
			given a lower case town name

			Returns: 
				String: correct town name
		"""
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

	def getFio(self, keyword, temp):
		""" 
			Function that returns a fio object 
			based on celcius of farenheit.

			Returns: 
				object: forecast io object with
				english or SI units.
		"""
		coords  = self.getCoords(keyword)
		if temp == "c":
			fio = ForecastIO.ForecastIO(darksky,
		                            units=ForecastIO.ForecastIO.UNITS_SI,
		                            lang=ForecastIO.ForecastIO.LANG_ENGLISH,
		                            latitude=coords[0], longitude=coords[1])
		else:
			fio = ForecastIO.ForecastIO(darksky,
		                            lang=ForecastIO.ForecastIO.LANG_ENGLISH,
		                            latitude=coords[0], longitude=coords[1])
		return fio

	def getDateForWeather(self, date):
		""" 
			Function that parses the date for 
			the weather section

			Returns: 
				string: date for weather section
		"""

		time    = datetime.fromtimestamp(date).strftime('%H:%M')
		hour    = int(time.split(":")[0])
		minutes = time.split(":")[1]
		date    = datetime.fromtimestamp(date).strftime('%a %d, %b %Y')
		if hour % 24 > 11:
			pm_or_am = " PM"
		else:
			pm_or_am = " AM"
		modded_hour = hour % 12 
		if modded_hour == 0:
			modded_hour = 12
		return date + " " + str(modded_hour) + ":" + minutes + pm_or_am

if __name__ == '__main__':
	Helper().getDateInEpoch("03/12/2017 00:00")