# !/usr/bin/env python
#  -*- coding: utf-8 -*-
from pprint import pprint
from helper import Helper
from random import randint
from forecastiopy import *
import json
import csv
import urllib2
import operator 
import datetime


class DataGathering:
	""" Class that gathers data from various data sources 
		TODO: EXPLICAR LA CLASE
		
	"""

	def __init__(self):
		self.helper = Helper()

	def getAEEData(self, key_1):
		""" 
			Funtion that reads a json file with energy related data and
			converts it into a format which can be readable by NVD3
			stacked chart. 

			Args:
				key_1 (str): The value for which we want to gather data.
				             This value comes from the energy.html file.

			Returns: 
				list: Contains 6 dictionaries. Each dictionary has a 
				key value (key_2 variable) and a value (values variable). 
				If an error occurs returns an empty array.
		"""

		# Variables
		suma         = 0  # Accumalator that holds the amount of data per year
		fiscal_year  = [] # Stores the year and the average amount of data per year
		values       = [] # Stores the fiscal year array for each key area
		result       = {} # Stores the value array and the key 2 variable
		final_result = [] # Stores the arrays of result
		
		try: 
			# Read energy related data and storing it in a dictionary
			with open('data/energy/AEE_SerieHistorica_2015.json') as data_file:
				energy_data = json.load(data_file)

			# Iterating through the file and storing the result
			for key_2 in energy_data[key_1]:

				for year in energy_data[key_1][key_2]:

					for month in energy_data[key_1][key_2][year]:
						suma += energy_data[key_1][key_2][year][month]

					fiscal_year.append(year)
					fiscal_year.append(suma/12)
					values.append(fiscal_year)
					fiscal_year  = []
					suma         = 0

				result["key"]    = key_2
				result["values"] = sorted(values)
				values           = []
				final_result.append(result)
				result           = {}

		except Exception as e:
			raise e
		finally:
			return final_result

	def getLoadData(self):

		""" 
			Function that reads load data in a csv file provided by 
			the NYISO. This data is then converted into a dictionary 
			and is returned.

			Returns: 
				dictionary: Contains a dictionary per month, day and a 
				list of the loads per hour in a given day.
		"""

		# Variables
		url           = 'http://mis.nyiso.com/public/dss/nyiso_loads.csv' # Url with the data
		response      = urllib2.urlopen(url)                              # Reading url
		load_data     = csv.reader(response)                              # Convering data to csv format
		year          = self.helper.getYear()                             # Current Year
		hourly_loads  = []                  # Stores the loads per hour
		daily_loads   = {}                  # Stores the loads per hour of a given day
		monthly_loads = {}                  # Stores the loads per day of a given month
		yearly_loads  = {}                  # Stores the monthly loads in a year

		# Converting data from csv to dictionary
		for row in load_data:

			# Ignoring first row
			if row[1] != "Month" and row[2] != "Day" and row[3] != 'Hr1':
				month = int(row[1])
				day   = int(row[2])

				# Getting hourly loads
				for i in range(3,27):
					try:
						hourly_loads.append(int(row[i]))
					# If there is an error reading the load then generate a 
					# random load value between 15000 and 25000
					except ValueError:
						pass
						hourly_loads.append((randint(15000,25000)))
				daily_loads[day]     = hourly_loads
				hourly_loads         = []
				monthly_loads[month] = daily_loads
				if self.helper.isEndOfMonth(month, day):
					daily_loads = {}

		yearly_loads[year] = monthly_loads

		return yearly_loads

	def getDataForLoadComparisons(self):
		""" 
			Function that reads a dictionary of load data and converts
			it into a format that is readable by NVD3.

			Returns: 
				dictionary: Dictionary of load data that will be visualized
				using NVD3
		"""

		# Variables
		load_data  = self.getLoadData() 
		values     = [] 
		inner_dict = {}
		outer_dict = {}
		final_data = []
		yesterday  = self.helper.getYesterday()
		key   = yesterday[0] + yesterday[1] + yesterday[2] + "-loadData"
		data  = load_data[yesterday[0]][int(yesterday[1])][int(yesterday[2])]
		dates = (['12:00 AM','1:00 AM','2:00 AM','3:00 AM','4:00 AM','5:00 AM',
			'6:00 AM','7:00 AM','8:00 AM','9:00 AM','10:00 AM','11:00 AM',
			'12:00 PM','1:00 PM','2:00 PM','3:00 PM','4:00 PM','5:00 PM',
			'6:00 PM','7:00 PM','8:00 PM','9:00 PM','10:00 PM','11:00 PM'])

		# Populating values array
		for i in range(0,len(data)):
			inner_dict['label'] = dates[i]
			inner_dict['value'] = data[i]
			values.append(inner_dict)
			inner_dict = {}

		# Populating the final_data array and returning it
		outer_dict['key'] = key
		outer_dict['values'] = values
		final_data.append(outer_dict)

		return final_data

	def getDayAheadMarketLBMPZonal(self):
		""" 
			Function that lbmp data in a csv file provided by 
			the NYISO. This data is then converted into a dictionary 
			and is returned.

			Returns: 
				dictionary of LBMP per New York zones.
		"""

		# Variables
		today   = self.helper.getYear() + self.helper.getMonth() + self.helper.getDay()
		url         = 'http://mis.nyiso.com/public/csv/damlbmp/'+today+'damlbmp_zone.csv' 
		response    = urllib2.urlopen(url)
		market_data = sorted(csv.reader(response), key=operator.itemgetter(1)) # Converting data to python csv
		counter     = 1 # Counter used for determining which hour we are curretly on
		lbmpZonal   = {}
		timestamp   = {}
		timestamps  = []
		market_info = {}

		# Converting csv data to market data and returning it
		for row in market_data:
			# Ignoring header row
			if row[0] != 'Time Stamp':
				market_info['LBMP ($/MWHr)']                     = float(row[3])
				market_info['Marginal Cost Losses ($/MWHr)']     = float(row[4])
				market_info['Marginal Cost Congestion ($/MWHr)'] = float(row[5])
				row[0]            = self.helper.getDateInEpoch(row[0])
				timestamp[row[0]] = market_info
				market_info       = {}
				timestamps.append(timestamp)
				timestamp         = {}
				counter           +=1
				# if counter == 23:
					# key = row[1]
				if counter == 24:
					lbmpZonal[row[1]] = timestamps
					timestamps        = []
					counter           = 1
		return lbmpZonal

	def getDataForLBMPZonalComparison(self):
		""" 
			Function that reads a dictionary of LBMP zonal data 
			and converts it into a format that is readable by NVD3.

			Returns: 
				dictionary: Dictionary of LBMP zonal data that 
				will be visualized using NVD3
		"""

		# Variables
		zonal_data       = self.getDayAheadMarketLBMPZonal()
		keys             = zonal_data.keys()
		final_data       = []
		values           = []
		outer_dictionary = {}
		inner_dictionary = {}

		# Populating final data array and returning it
		for key in keys:
			for data in zonal_data[key]:
				inner_dictionary['x'] = data.keys()[0]
				inner_dictionary['y'] = data[data.keys()[0]]['LBMP ($/MWHr)']
				values.append(inner_dictionary)
				inner_dictionary = {}
			outer_dictionary['values'] = values
			values = []
			outer_dictionary['key']    = key
			final_data.append(outer_dictionary)
			outer_dictionary = {}

		return final_data

	def getDataForLBMPvsLoadComparisons(self):
		""" 
			Function that reads a dictionary of load data and
			another dictionary of  LBMP zonal data and converts 
			it into a format that is readable by NVD3.

			Returns: 
				dictionary: Dictionary of load and
				LBMP zonal data that will be visualized using NVD3
		"""

		# Variables
		lbmp_data    = self.getDataForLBMPZonalComparison()[14] # Getting CAPITL zone
		load_data    = self.getLoadData()
		final_data   = []
		lbmp_dict    = {}
		load_dict    = {}
		load_values  = []
		dates        = []
		price_values = []

		# Getting needed lbmp_data
		key = "LBMP ($/MWHr) in " + lbmp_data['key']
		for value in lbmp_data['values']:
			dates_and_prices = []
			dates_and_prices.append(value['x'])
			dates.append(value['x'])
			dates_and_prices.append(value['y'])
			price_values.append(dates_and_prices)
		lbmp_dict['key'] = key
		lbmp_dict['values'] = price_values
		final_data.append(lbmp_dict)
		data_dict = {}

		# Getting needed load data
		yesterday = self.helper.getYesterday()
		loads = load_data[yesterday[0]][int(yesterday[1])][int(yesterday[2])]
		print len(loads),len(dates)
		for i in range(0,len(loads)):
			dates_and_loads = []
			dates_and_loads.append(dates[i])
			dates_and_loads.append(loads[i])
			load_values.append(dates_and_loads)
		load_dict['key'] = lbmp_data['key'] + " Area Loads"
		load_dict['values'] = load_values
		load_dict['bar'] = 'True'
		final_data.append(load_dict)
		return final_data

	def getHourlyWeather(self, keyword, temp, last_hour):
		""" 
			Function that gets hourly weather data from
			dark sky API for the next 12 hours. 

			Returns: 
				array: 12 hour weather forcast.
				Contains 12 dictionaries with the following:
					icon: used for visualizing current weather
					summary: sentence describing current weather
					temperature: current temperature in F or C
					humidity: current humidilty percentage
					time: date for weather
					precipProbability: precipitation probability
					wind: The wind speed and direction
		"""

		# Variables
		conditions = []
		weather    = {}

		fio = self.helper.getFio(keyword, temp) # Getting fio object

		if fio.has_hourly() is True:
			hourly = FIOHourly.FIOHourly(fio)

			# Getting weather forecast for next 12 hours
			for hour in xrange(1, last_hour):
				for item in hourly.get_hour(hour).keys():
					# Parsing data from hourly fio object and adding it to weather dictionary
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
						weather[item] = self.helper.getDateForWeather(hourly.get_hour(hour)[item])
					if item == "precipProbability":
						weather[item] = str(hourly.get_hour(hour)[item] * 100).split(".")[0] + "%"
					if item == "windSpeed":
						windSpeed = unicode(hourly.get_hour(hour)[item])
					if item == "windBearing":
						windBearing     = unicode(hourly.get_hour(hour)[item])
						windBearing     = self.helper.convertWindBearing(windBearing)
						weather["wind"] = windBearing + " " + windSpeed + " mph"

				# Populating conditions array with weather dicitonary
				conditions.append(weather)
				weather = {}
		else:
			return 'No hourly data'
		return conditions

	def getHourlyWeatherInCSV(self, keyword, temp):
		""" 
			Function that gets hourly weather data from
			dark sky API for the next 24 hours and stores 
			it in a csv file. 

			Returns: 
				void: csv file with hourly forecast for the next 24 hours.
				File name will be <town>_<c or f>.csv
		"""
		conditions = self.getHourlyWeather(keyword, temp, 25)
		
		if keyword[0] == "0":
			keyword = self.helper.convertZipcodeToTown(keyword)
		# keyword = self.helper.getCorrectTownName(keyword)
		if temp == 'f':
			filename = "data/weather/"+keyword+"_f.csv"
		else:
			filename = "data/weather/"+keyword+"_c.csv"
		f = csv.writer(open(filename, "wb+"))
		f.writerow(["date", "description", "precipitation", "temperature", "humidity", "wind", "icon"])
		for condition in conditions:
			temp = condition['temperature'].split(" ")[0][:-2] + " " + condition['temperature'].split(" ")[1]
			try:
				f.writerow([condition['time'],
					condition['summary'],
					condition['precipProbability'],
					temp,
					condition['humidity'],
					condition['wind'],
					condition['icon']])
			except:
				pass

	def getHourlyPrecip(self, keyword):
		""" 
			Function that returns an array of dicitionaries that
			contain hourly precipitation.

			Return:
				Array: filled with dictionary that have the 
				following:
					x: the time in epoch where it occured
					y: the float value of the precipitation
		"""

		weather_data  = self.getHourlyWeather(keyword, "f", 25)
		precip_values = [] # Array that will contain all the precipitation data
		precip_data   = {} # Dictionary of precipitation data

		# Getting precipiation data
		for data in weather_data:
			precip_data["x"] = self.helper.getDateInEpoch(data["time"])
			precip_data["y"] = float(data["precipProbability"][:-1])/100
			precip_values.append(precip_data)
			precip_data = {}

		return precip_values

	def getHourlyHumidity(self, keyword):
		""" 
			Function that returns an array of dicitionaries that
			contain hourly humidity.

			Return:
				Array: filled with dictionary that have the 
				following:
					x: the time in epoch where it occured
					y: the float value of the humidity
		"""

		weather_data    = self.getHourlyWeather(keyword, "f", 25)
		humidity_values = [] # Array that will contain all the humidity data
		humidity_data   = {} # Dictionary of humidity data

		# Getting humidity data
		for data in weather_data:
			humidity_data["x"] = self.helper.getDateInEpoch(data["time"])
			humidity_data["y"] = float(data["humidity"][:-1])/100
			humidity_values.append(humidity_data)
			humidity_data = {}

		return humidity_values

	def getHourlyWind(self, keyword):
		""" 
			Function that returns an array of dicitionaries that
			contain hourly wind.

			Return:
				Array: filled with dictionary that have the 
				following:
					x: the time in epoch where it occured
					y: the float value of the wind
		"""

		weather_data = self.getHourlyWeather(keyword, "f", 25)
		wind_values  = [] # Array that will contain all the wind data
		wind_data    = {} # Dictionary of wind data

		# Getting humidity data
		for data in weather_data:
			wind_data["x"] = self.helper.getDateInEpoch(data["time"])
			wind_data["y"] = float(data["wind"].split(" ")[1])
			wind_values.append(wind_data)
			wind_data = {}

		return wind_values

	def getHourlyTemp(self, keyword, deg):
		""" 
			Function that returns an array of dicitionaries that
			contain hourly temperature based on degree (C or F).

			Return:
				Array: filled with dictionary that have the 
				following:
					x: the time in epoch where it occured
					y: the float value of the temperature in C or F
		"""

		weather_data = self.getHourlyWeather(keyword, deg, 25)
		temp_values  = [] # Array that will contain all the temperature data
		temp_data    = {} # Dictionary of temperature data

		# Getting temperature data
		for data in weather_data:
			temp_data["x"] = self.helper.getDateInEpoch(data["time"])
			temp_data["y"] = float(data["temperature"].split("°")[0])
			temp_values.append(temp_data)
			temp_data      = {}

		return temp_values

	def getTodaysWeather(self, keyword, temp):
		""" 
			Function that returns today's weather given 
			a towns name or zipcode from the dark sky API. 

			Returns: 
				dictionary: Contains a dictionary with the following:
					current: current weather
					icon: used for visualizing current weather
					precipProbability: precipitation probability
					summary: sentence describing current weather
					sunriseTime: sunrise date
					sunsetTime: sunset time
					temperature: current temperature in F or C
					temperatureMax: max temperature in F or C
					temperatureMin: min temperature in F or C
					humidity: current humidilty percentage
					town: the town name
					wind: The wind speed and direction
		"""

		# Variables
		weather = {} 
		fio     = self.helper.getFio(keyword, temp) # Getting fio object
		
		# Getting todays weather data and populating the dictionary
		if fio.has_daily() is True and fio.has_hourly() is True:
		    daily  = FIODaily.FIODaily(fio)
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
						windBearing = self.helper.convertWindBearing(windBearing)
					if item == "sunsetTime":
						weather[item] = self.helper.getDateForWeather(daily.get_day(day)[item])
					if item == "sunriseTime":
						weather[item] = self.helper.getDateForWeather(daily.get_day(day)[item])
					if item == "precipProbability":
						weather[item] = str(daily.get_day(day)[item] * 100).split(".")[0] + "%"
				weather["wind"] = windBearing + " " + windSpeed + " mph"
				for item in hourly.get_hour(day).keys():
					if item == "summary":
						weather["current"] = unicode(hourly.get_hour(0)[item])
					if item == "temperature":
						weather[item] = str(hourly.get_hour(0)[item]).split(".")[0]
					if item == "icon":
						weather[item] = unicode(hourly.get_hour(0)[item])
				weather["town"] = self.helper.getCoords(keyword)[2]
		else:
			return 'No Todays data'

		return weather

	def getDailyWeather(self, keyword, temp):
		""" 
			Function that returns weather forecast for the
			next 4 days given a towns name or zipcode from 
			the dark sky API. 

			Returns: 
				array: Contains 4 dictionaries with the following:
					summary: sentence describing current weather
					icon: used for visualizing current weather
					current: current weather
					temperatureMax: max temperature in F or C
					temperatureMin: min temperature in F or C
					precipProbability: precipitation probability
					time: date of the weather forecast
					sunriseTime: sunrise date
					sunsetTime: sunset time
					temperature: current temperature in F or C
		"""

		# Variables
		daily_weather = []
		weather       = {}
		fio           = self.helper.getFio(keyword, temp) # Getting fio object

		# Getting 4-day forecast, storing each day's data in a dictionary and
		# storing each dictionary in an array
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
						weather[item] = self.helper.getDateForWeather(daily.get_day(day)[item])
				daily_weather.append(weather)
				weather = {}
		else:
			return 'No Daily data'
		return daily_weather

	def getHourlyLoads(self):
		""" 
			Function that returns an array of dicitionaries that
			contain hourly loads on NYISO.

			Return:
				Array: filled with dictionary that have the 
				following:
					x: the time in epoch where it occured
					y: the float value of the load
		"""

		loads_data   = self.getDataForLoadComparisons()
		load_values  = [] # Array that will contain all the load data
		load_data    = {} # Dictionary of load data

		# Parsing load data
		today = self.helper.getYear() + self.helper.getMonth() + self.helper.getDay()
		for data in loads_data[0]['values']:
			load_data["x"] = self.helper.getDateInEpoch(today + " " + data["label"])
			load_data["y"] = float(data["value"])
			load_values.append(load_data)
			load_data      = {}

		return load_values

	def getHourlyZonalLBMP(self, zone):
		""" 
			Function that returns an array of dicitionaries that
			contain hourly lbmp based a user selected zone.
			Data is collected from NYISO.

			Return:
				Array: filled with dictionary that have the 
				following:
					x: the time in epoch where it occured
					y: the float value of the lbmp data
		"""

		lbmp_data = self.getDataForLBMPZonalComparison()

		# Parsing lbmp data
		for data in lbmp_data:
			if data["key"] == zone:
				return data["values"]


if __name__ == '__main__':
	data = DataGathering()
	# pprint(data.getDayAheadMarketLBMPZonal())
	pprint(data.getHourlyZonalLBMP("CAPITL"))
	# pprint(data.getHourlyTemp(u"mayaguez","f"))