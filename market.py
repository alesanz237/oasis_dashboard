#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import urllib2
from pprint import pprint
import operator
import time

def getLoadData():
	url = 'http://mis.nyiso.com/public/dss/nyiso_loads.csv'
	response = urllib2.urlopen(url)
	load_data = csv.reader(response)
	year = '2017'
	hourly_loads = []
	daily_loads = {}
	monthly_loads = {}
	yearly_loads = {}
	for row in load_data:
		if row[1] != "Month" and row[2] != "Day" and row[3] != 'Hr1':
			month = int(row[1])
			day   = int(row[2])
			for i in range(3,27):
				hourly_loads.append(int(row[i]))
			daily_loads[day] = hourly_loads
			hourly_loads = []
			monthly_loads[month] = daily_loads
			if ((month == 1 and day == 31) or (month == 2 and day == 28)  or
				(month == 3 and day == 31) or (month == 4 and day == 30)  or
				(month == 5 and day == 31) or (month == 6 and day == 30)  or
				(month == 7 and day == 31) or (month == 8 and day == 31)  or
				(month == 9 and day == 30) or (month == 10 and day == 31) or
				(month == 11 and day == 30) or (month == 12 and day == 31)):
				daily_loads = {}
	yearly_loads[year] = monthly_loads
	return yearly_loads
		# print row[1]

def getDayAheadMarketLBMPZonal():
	## dd/mm/yyyy format
	current_date = time.strftime("%Y%m%d")
	url = 'http://mis.nyiso.com/public/csv/damlbmp/'+time.strftime("%Y%m%d")+'damlbmp_zone.csv'
	response = urllib2.urlopen(url)
	market_data = sorted(csv.reader(response), key=operator.itemgetter(1))
	counter = 0
	lbmpZonal = {}
	timestamp = {}
	timestamps = []
	market_info = {}
	for row in market_data:
		if row[0] != 'Time Stamp':
			market_info['LBMP ($/MWHr)'] = row[3]
			market_info['Marginal Cost Losses ($/MWHr)'] = row[4]
			market_info['Marginal Cost Congestion ($/MWHr)'] = row[5]
			timestamp[row[0]] = market_info
			market_info = {}
			timestamps.append(timestamp)
			timestamp = {}
			counter +=1
			if counter == 24:
				lbmpZonal[row[1]] = timestamps
				timestamps = []
				counter = 0		
	return lbmpZonal
			


if __name__ == '__main__':
	pprint(getLoadData())
	pprint(getDayAheadMarketLBMPZonal())