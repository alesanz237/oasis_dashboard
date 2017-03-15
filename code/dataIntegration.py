# !/usr/bin/env python
#  -*- coding: utf-8 -*-
from dataGathering import DataGathering

class DataForComparison:
	""" class that generates a graph based on user selected comparisons """

	def __init__(self):
		self.data    = DataGathering()
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
			generated in the generateData method.

		"""

		# Users selects 4 datasets
		if len(selects)  == 4:
			self.dataset.append(self.generateData(selects[0]))
			self.dataset.append(self.generateData(selects[1]))
			self.dataset.append(self.generateData(selects[2]))
			self.dataset.append(self.generateData(selects[3]))

		# User selects 3 datasets
		elif len(selects) == 3:
			self.dataset.append(self.generateData(selects[0]))
			self.dataset.append(self.generateData(selects[1]))
			self.dataset.append(self.generateData(selects[2]))

		# User select 2 datasets
		elif len(selects) == 2:
			self.dataset.append(self.generateData(selects[0]))
			self.dataset.append(self.generateData(selects[1]))

		# User selects 1 dataset
		else:
			self.dataset.append(self.generateData(selects[0]))

	def generateData(self,dataset):
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
			town = dataset[1]
			data["key"] = identifier + "_" + town
			precip_data = self.data.getHourlyWeather(town,"f")
			print precip_data
			
		# Getting humidity dataset
		elif identifier == "humidity":
			town = dataset[1]
			data["key"] = identifier + "_" + town

		# Getting wind dataset
		elif identifier == "wind":
			town = dataset[1]
			data["key"] = identifier + "_" + town

		# Getting temperature dataset
		elif identifier == "temp":
			town = dataset[1]
			deg  = dateset[2]

		# Getting load based marginal pricing dataset
		elif identifier == "lbmp":
			zone = dataset[1]

		# # Getting load dataset
		# elif identifier == "load":

		# # Getting positive tweets dataset
		# elif identifier == "pos":

		# # Getting negative tweets dataset
		# elif identifier == "neg":

		

	# def getSelectStatus(self):
	# 	""" 
	# 		Return select status
	# 	"""
	# 	print self.select1
	# 	print self.select2
	# 	print self.select3
	# 	print self.select4 

	def getData(self):
		""" 
			Getter for data attribute

			Returns: 
				dictionary of LBMP per New York zones.
		"""

		return self.data()

if __name__ == '__main__':
	comparator = DataForComparison()
	comparator.addData([u"precip_mayaguez"])