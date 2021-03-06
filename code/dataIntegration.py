# !/usr/bin/env python
#  -*- coding: utf-8 -*-
from dataGathering import DataGathering
from helper import Helper
from params import towns, load_zones
import csv
from sentimentAnalysis import getPositiveTweetsPerHour, getNegativeTweetsPerHour
from pprint import pprint

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

		# Generating csv file
		self.generateCSVFile()

	def getData(self,dataset):
		""" 
			Generates dictionary based on the user selected 
			dataset.
			User may select the following datasets:
			1. "pos_tweets" : amount of positive tweets per hour for a day
			2. "neg_tweets" : amount of negative tweets per hour for a day
			3. "precip_<town>": precipitation per hour for a day for a given town
			4. "cloudCover_<town>": cloud coverage per hour for a day for a given town
			5. "temp_<town>_<deg>": temperature in F or C per hour for a day for a give town
			6. "humidity_<town>": humidity per hour for a day for a given town
			7. "wind_<town>": wind per hour for a day for a given town:
			8. "load": Loads per hour for a day from NYISO
			9. "lmbp_<zone>": lbmp per hor for a day from NYISO

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
			# print identifier+"_"+town
			# print self.data.getHourlyPrecip(town)
			data["key"]    = identifier+"_"+town
			# print data["key"]
			data["values"] = self.data.getHourlyPrecip(town)

		# Getting cloud coverage dataset
		if identifier == "cloudCover":
			town           = dataset[1]
			data["key"]    = identifier+"_"+town
			data["values"] = self.data.getHourlyCloudCoverage(town)
			
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

		# Getting load dataset
		elif identifier == "load":
			data["key"]    = identifier
			data["values"] = self.data.getHourlyLoads()

		# Getting positive tweets dataset
		elif identifier == "pos":
			data = getPositiveTweetsPerHour()

		# Getting negative tweets dataset
		elif identifier == "neg":
			data = getNegativeTweetsPerHour()

		return data

	def setSelectValues(self):
		""" Sets dictionary of select values """
		self.select_values = ({"":" ",
							    "pos":"Positive tweets",
							    "neg":"Negative tweets",
							    "precip":"Precipitation data",
							    "temp":"Temperature data",
							    "humidity":"Humidity data",
							    "cloudCover":"Cloud coverage",
							    "wind":"Wind data",
							    "load":"Load data",
							    "lbmp":"Load based marginal pricing data"})
		self.select_values2 = ({"":" ",
							    "pos":"Positive tweets",
							    "neg":"Negative tweets",
							    "precip":"Precipitation data",
							    "temp":"Temperature data",
							    "humidity":"Humidity data",
							    "cloudCover":"Cloud coverage",
							    "wind":"Wind data",
							    "load":"Load data",
							    "lbmp":"Load based marginal pricing data"})
		self.select_values3 = ({"":" ",
							    "pos":"Positive tweets",
							    "neg":"Negative tweets",
							    "precip":"Precipitation data",
							    "temp":"Temperature data",
							    "humidity":"Humidity data",
							    "cloudCover":"Cloud coverage",
							    "wind":"Wind data",
							    "load":"Load data",
							    "lbmp":"Load based marginal pricing data"})
		self.select_values4 = ({"":" ",
							    "pos":"Positive tweets",
							    "neg":"Negative tweets",
							    "precip":"Precipitation data",
							    "temp":"Temperature data",
							    "humidity":"Humidity data",
							    "cloudCover":"Cloud coverage",
							    "wind":"Wind data",
							    "load":"Load data",
							    "lbmp":"Load based marginal pricing data"})
		self.dataset = []

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

	def getDataset(self):
		"""
			Return normalized dataset array for visualization
		"""
		# self.normalizeDataset()
		return self.dataset

	def generateCSVFile(self):
		"""
			Funtion that generates a csv file with the 
			selected datasets by the user and stores it in 
			integrated_data folder.
		"""

		keys   = []
		dates  = []
		values = []

		filename = "data/integrated_data/graph_dataset.csv"
		i        = 0

		# Getting keys, dates and values
		keys.append("date")
		for dataset in self.dataset:
			keys.append(dataset["key"])
			for data in dataset["values"]:
				if i < 24:
					dates.append(self.helper.convertDateFromEpoch(data["x"]))
				i+=1
				values.append(data["y"])
					
		
		f = csv.writer(open(filename, "wb+"))
		f.writerow(keys)
		if len(self.dataset) == 4:
			for i in range(0,len(dates)):
				f.writerow([dates[i],
						   values[i],
						   values[i+24],
						   values[i+48],
						   values[i+72]])
		elif len(self.dataset) == 3:
			for i in range(0,len(dates)):
				print dates[i]
				print 
				f.writerow([dates[i],
						   values[i],
						   values[i+24],
						   values[i+48]])
		elif len(self.dataset) == 2:
			for i in range(0,len(dates)):
				f.writerow([dates[i],
					       values[i],
						   values[i+24]])

		elif len(self.dataset) == 1:
			for i in range(0,len(dates)):
				f.writerow([dates[i],values[i]])

	def importDataFromCSV(self):
		"""
			Functions that reads a csv file and adds
			the data to the DataIntegration class
		"""
		file         = "data/uploads/graph_dataset.csv"
		csv_data     = []
		integrated_data = []
		outer_data      = {}
		values          = []
		inner_data      = {}

		counter = 0

		# Reading csv file and storing data in file
		with open(file) as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				csv_data.append(row) 

		# print csv_data
		# Getting data that is needed for visualization
		keys =  csv_data[0].keys()[1:]
		# print keys
		for key in keys:
			for data in csv_data:
				if key in data and counter < 24:
					inner_data["x"] = self.helper.getDateInEpoch(data["date"])
					# print type(float(data[key]))
					inner_data["y"] = float(data[key])
					values.append(inner_data)
					counter += 1
					inner_data = {}
				if counter == 24:
					outer_data["values"] = values
					outer_data["key"]    = key
					counter = 0
					values = []
					integrated_data.append(outer_data)
					outer_data = {}

		self.dataset = integrated_data

		# pprint(integrated_data)

if __name__ == '__main__':
	comparator = DataIntegration()
	comparator.addData([u"cloudCover_aguada",u"load"])
	pprint(comparator.getDataset())
	# pprint(comparator.dataset)
	# comparator.generateCSVFile()
	# comparator.importDataFromCSV()
	# pprint(comparator.normalizeDataset())