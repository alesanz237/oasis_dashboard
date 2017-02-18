#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import urllib2
from pprint import pprint
import operator
import calendar
import time
from random import randint

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
				try:
					hourly_loads.append(int(row[i]))
				except ValueError:
					pass
					hourly_loads.append((randint(15000,25000)))
					# print row[i], type(row[i])
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

def getDayAheadMarketLBMPZonal():
	## dd/mm/yyyy format
	current_date = time.strftime("%Y%m%d")
	current_day = int(time.strftime("%d"))-1
	yesterday = time.strftime("%Y%m") + str(current_day)
	if current_day == 0:
		current_year = int(time.strftime("%Y"))
		current_month = int(time.strftime("%m")) -1
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
			current_year = int(time.strftime("%Y")) - 1
		yesterday = str(current_year)+str(current_month)+str(current_day)


	url = 'http://mis.nyiso.com/public/csv/damlbmp/'+yesterday+'damlbmp_zone.csv'
	response = urllib2.urlopen(url)
	market_data = sorted(csv.reader(response), key=operator.itemgetter(1))
	counter = 0
	lbmpZonal = {}
	timestamp = {}
	timestamps = []
	market_info = {}
	for row in market_data:
		if row[0] != 'Time Stamp':
			market_info['LBMP ($/MWHr)'] = float(row[3])
			market_info['Marginal Cost Losses ($/MWHr)'] = float(row[4])
			market_info['Marginal Cost Congestion ($/MWHr)'] = float(row[5])
			row[0] = calendar.timegm(time.strptime(row[0],'%m/%d/%Y %H:%M'))
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
			
def getDataForLBMPZonalComparison():
	zonal_data = getDayAheadMarketLBMPZonal()
	keys = zonal_data.keys()
	final_data = []
	values = []
	outer_dictionary = {}
	inner_dictionary = {}
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

def getDataForLoadComparisons():
	load_data = getLoadData()
	# return load_data
	values = []
	inner_dict = {}
	outer_dict = {}
	final_data = []

	current_date = time.strftime("%Y%m%d")
	current_day = int(time.strftime("%d"))-1
	current_month = int(time.strftime("%m"))
	current_year = int(time.strftime("%Y"))
	yesterday = time.strftime("%Y%m") + str(current_day)
	if current_day == 0:
		current_year = int(time.strftime("%Y"))
		current_month = int(time.strftime("%m")) -1
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
			current_year = int(time.strftime("%Y")) - 1
		yesterday = str(current_year)+str(current_month)+str(current_day)

	key = yesterday + "-loadData"
	data = load_data[str(current_year)][current_month][current_day]
	dates = ['12:00 AM','1:00 AM','2:00 AM','3:00 AM','4:00 AM','5:00 AM','6:00 AM','7:00 AM','8:00 AM','9:00 AM','10:00 AM','11:00 AM','12:00 PM','1:00 PM','2:00 PM','3:00 PM','4:00 PM','5:00 PM','6:00 PM','7:00 PM','8:00 PM','9:00 PM','10:00 PM','11:00 PM']
	for i in range(0,len(data)):
		inner_dict['label'] = dates[i]
		inner_dict['value'] = data[i]
		values.append(inner_dict)
		inner_dict = {}
	outer_dict['key'] = key
	outer_dict['values'] = values
	final_data.append(outer_dict)
	return final_data

def getDataForLBMPvsLoadComparisons():
	lbmp_data = getDataForLBMPZonalComparison()[14]
	load_data = getLoadData()
	final_data = []
	lbmp_dict = {}
	load_dict = {}
	load_values = []
	dates = []
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
	current_date = time.strftime("%Y%m%d")
	current_day = int(time.strftime("%d"))-1
	current_month = int(time.strftime("%m"))
	current_year = int(time.strftime("%Y"))
	if current_day == 0:
		current_year = int(time.strftime("%Y"))
		current_month = int(time.strftime("%m")) -1
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
			current_year = int(time.strftime("%Y")) - 1
	loads = load_data[str(current_year)][current_month][current_day]
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



# if __name__ == '__main__':
	# pprint(getLoadData())
	# pprint(getDayAheadMarketLBMPZonal())
	# pprint(getDayAheadMarketLBMPZonal())
	# pprint(getDataForLBMPZonalComparison())
	# pprint(getDataForLoadComparisons())
	# pprint(getDataForLBMPvsLoadComparisons())