# !/usr/bin/env python
#  -*- coding: utf-8 -*-
from dataGathering import DataGathering
from helper import Helper
from params import towns, load_zones

class DataIntegration:
	""" class that gets a graph based on user selected comparisons """

	def __init__(self):
		self.data           = DataGathering()
		self.helper         = Helper()
		self.select_values  = {}
		self.select_values2 = {}
		self.select_values3 = {}
		self.select_values4 = {}
		self.dataset = []

	def addData(self,selects):
		""" 
			Adds a dicitionary to dataset element. The amount
			of dictionaries depends on how many selects does
			the user want to compare. The dictionary is 
			getd in the getData method.

		"""

		# Users selects 4 datasets
		if len(selects)  == 4:
			self.dataset.append(self.getData(selects[0]))
			self.dataset.append(self.getData(selects[1]))
			self.dataset.append(self.getData(selects[2]))
			self.dataset.append(self.getData(selects[3]))

		# User selects 3 datasets
		elif len(selects) == 3:
			self.dataset.append(self.getData(selects[0]))
			self.dataset.append(self.getData(selects[1]))
			self.dataset.append(self.getData(selects[2]))

		# User select 2 datasets
		elif len(selects) == 2:
			self.dataset.append(self.getData(selects[0]))
			self.dataset.append(self.getData(selects[1]))

		# User selects 1 dataset
		else:
			self.dataset.append(self.getData(selects[0]))

	def getData(self,dataset):
		""" 
			Generates dictionary based on the user selected 
			dataset.
			User may select the following datasets:
			1. "pos_tweets" : amount of positive tweets per hour for a day
			2. "neg_tweets" : amount of negative tweets per hour for a day
			3. "precip_<town>": precipitation per hour for a day for a given town
			4. "temp_<town>_<deg>": temperature in F or C per hour for a day for a give town
			5. "humidity_<town>": humidity per hour for a day for a given town
			6. "wind_<town>": wind per hour for a day for a given town:
			7. "load": Loads per hour for a day from NYISO
			8. "lmbp_<zone>": lbmp per hor for a day from NYISO

			Returns:
				Dictionary: Dictionary of data that will be added 
		"""

		# Variables
		dataset    = dataset.split("_")
		identifier = dataset[0]
		data       = {}

		# Getting precipitation dataset
		if identifier == "precip":
			town           = dataset[1]
			data["key"]    = identifier + "_" + self.helper.getCoords(town)[2]
			data["values"] = self.data.getHourlyPrecip(town)
			
		# Getting humidity dataset
		elif identifier == "humidity":
			town           = dataset[1]
			data["key"]    = identifier + "_" + self.helper.getCoords(town)[2]
			data["values"] = self.data.getHourlyHumidity(town)

		# Getting wind dataset
		elif identifier == "wind":
			town           = dataset[1]
			data["key"]    = identifier + "_" + self.helper.getCoords(town)[2]
			data["values"] = self.data.getHourlyWind(town)

		# Getting temperature dataset
		elif identifier == "temp":
			town           = dataset[1]
			deg            = dataset[2]
			data["key"]    = identifier + "_" + self.helper.getCoords(town)[2] + "_" + deg
			data["values"] = self.data.getHourlyTemp(town,deg)

		# Getting load based marginal pricing dataset
		elif identifier == "lbmp":
			zone = dataset[1]
			data["key"] = identifier + "_" + zone
			data["values"] = self.data.getHourlyZonalLBMP(zone)

		# # Getting load dataset
		elif identifier == "load":
			data["key"]    = identifier
			data["values"] = self.data.getHourlyLoads()

		# # Getting positive tweets dataset
		# elif identifier == "pos":

		# # Getting negative tweets dataset
		# elif identifier == "neg":

		return data

	def setSelectValues(self):
		""" Sets dictionary of select values """
		self.select_values = ({"":" ",
							    "pos":"Positive Tweets",
							    "neg":"Negative Tweets",
							    "precip":"Precipitation data",
							    "temp":"Temperature data",
							    "humidity":"Humidity data",
							    "wind":"Wind data",
							    "load":"Load data",
							    "lbmp":"Load based marginal pricing data"})
		self.select_values2 = ({"":" ",
							    "pos":"Positive Tweets",
							    "neg":"Negative Tweets",
							    "precip":"Precipitation data",
							    "temp":"Temperature data",
							    "humidity":"Humidity data",
							    "wind":"Wind data",
							    "load":"Load data",
							    "lbmp":"Load based marginal pricing data"})
		self.select_values3 = ({"":" ",
							    "pos":"Positive Tweets",
							    "neg":"Negative Tweets",
							    "precip":"Precipitation data",
							    "temp":"Temperature data",
							    "humidity":"Humidity data",
							    "wind":"Wind data",
							    "load":"Load data",
							    "lbmp":"Load based marginal pricing data"})
		self.select_values4 = ({"":" ",
							    "pos":"Positive Tweets",
							    "neg":"Negative Tweets",
							    "precip":"Precipitation data",
							    "temp":"Temperature data",
							    "humidity":"Humidity data",
							    "wind":"Wind data",
							    "load":"Load data",
							    "lbmp":"Load based marginal pricing data"})

	def getSelectValues(self, select):
		""" Returns dictionary of select values """
		select_values = {}
		if int(select) == 0:
			select_values = self.select_values
		elif int(select) == 1:
			select_values = self.select_values2
		elif int(select) == 2:
			select_values = self.select_values3
		elif int(select) == 3:
			select_values = self.select_values4
		return select_values

	def updateSelectValues(self,select,selected_value):
		""" 
			Function that removes a user selected value
			from the select_values dictionary
		"""

		if int(select) == 1:
			del self.select_values2[selected_value]
			del self.select_values3[selected_value]
			del self.select_values4[selected_value]


		elif int(select) == 2:
			del self.select_values3[selected_value]
			del self.select_values4[selected_value]

		elif int(select) == 3:
			del self.select_values4[selected_value]
		
	def getTowns(self):
		"""
			Function that returns the town of Puerto Rico
		"""
		return towns

	def getLoadZones(self):
		"""
			Function that retunrs NY load zones
		"""
		return load_zones

# if __name__ == '__main__':
	# comparator = DataIntegration()
	# comparator.updateSelectValues("pos")
	# print comparator.getTowns()
	# comparator.setSelectValues()
	# comparator.updateSelectValues(1,"load")
	# print comparator.getSelectValues(0)
	# print comparator.select_values
# 	comparator.addData([u"lbmp_CAPITL"])
# 	print comparator.dataset