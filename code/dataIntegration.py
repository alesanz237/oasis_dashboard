# !/usr/bin/env python
#  -*- coding: utf-8 -*-
from dataGathering import DataGathering
from helper import Helper

class DataForComparison:
	""" class that gets a graph based on user selected comparisons """

	def __init__(self):
		self.data    = DataGathering()
		self.helper  = Helper()
		# self.select1 = False
		# self.select2 = False 
		# self.select3 = False
		# self.select4 = False
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

if __name__ == '__main__':
	comparator = DataForComparison()
	comparator.addData([u"lbmp_CAPITL"])
	print comparator.dataset