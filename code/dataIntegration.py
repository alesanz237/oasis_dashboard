# !/usr/bin/env python
#  -*- coding: utf-8 -*-
from weather import getHourlyWeather
from market import getLoadData, getDayAheadMarketLBMPZonal
from sentimentAnalysis import getTweetsLen

class DataForComparison:
	""" class that generates a graph based on user selected comparisons """

	def __init__(self):
		self.select1 = False
		self.select2 = False 
		self.select3 = False
		self.select4 = False
		self.data    = []

	def addData(self,selects):
		""" Add data to graph portion """
		for select in selects:
			if self.select1 != True:
				self.data.append(self.generateData(select,1))
			elif self.select2 != True:
				self.data.append(self.generateData(select,2))
			elif self.select3 != True:
				self.data.append(self.generateData(select,3))
			elif self.select4 != True:
				self.data.append(self.generateData(select,4))

	def generateData(self,select,select_number):
		""" Gets data that will be added to class data list """

		if select == "pos_tweets":
			y = getTweetsLen()[0]
		elif select == "neg_tweets":
			y = getTweetsLen()[1]

		if select_number == 1:
			self.select1 = True
		if select_number == 2:
			self.select2 = True
		if select_number == 3:
			self.select3 = True
		if select_number == 4:
			self.select4 = True

	def getSelectStatus(self):
		print self.select1
		print self.select2
		print self.select3
		print self.select4 

	def getData(self):
		""" Getter for data attribute """
		return self.data()

if __name__ == '__main__':
	comparator = DataForComparison()
	selects = ["pos_tweets","neg_tweets"]
	comparator.addData(selects)
	comparator.getSelectStatus()