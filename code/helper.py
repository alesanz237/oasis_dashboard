#!/usr/bin/env python
# -*- coding: utf-8 -*-

from params import lat_lon_towns
import json
from pprint import pprint
import time
import urllib2
import datetime
import sys  # Library needed for working with utf8 characters
reload(sys)  # Reseting system
sys.setdefaultencoding('utf8') # Setting the default encoding to utf8

def getKey1():
	key_1 = []
	with open('./data/AEE_SerieHistorica_2015.json') as data_file:
		energy_data = json.load(data_file)
	for dataset in energy_data:
		key_1.append(dataset)
	return key_1

def getKey2(key_1):
	key_2 = []
	with open('./data/AEE_SerieHistorica_2015.json') as data_file:
		energy_data = json.load(data_file)
	for dataset in energy_data[key_1]:
		key_2.append(dataset)
	return key_2

def getAEEData(key_1):
	fiscal_year = []
	final_result = []
	values = []
	result = {}
	suma = 0
	with open('./data/AEE_SerieHistorica_2015.json') as data_file:
		energy_data = json.load(data_file)
	for key_2 in energy_data[key_1]:
		for year in energy_data[key_1][key_2]:
			for month in energy_data[key_1][key_2][year]:
				suma +=energy_data[key_1][key_2][year][month]
			# print year, suma/12
			fiscal_year.append(year)
			fiscal_year.append(suma/12)
			values.append(fiscal_year)
			fiscal_year = []
			suma = 0
		result["key"] = key_2
		result["values"] = sorted(values)
		values = []
		final_result.append(result)
		result = {}
		# print final_resultx
	return final_result
		
def getMarketHistory(symbol, data_type, date):
	# data_type can be daily, monthly & yearly
	# print "Hello from getMarketHistory"
	day = date.split("-")[2]
	month = date.split("-")[1]
	year = str(int(date.split("-")[0])-1)
	new_date = year+month+day
	# print new_date
	final_result=[]
	results = {}
	results["values"] = []
	result = {}
	url = "http://marketdata.websol.barchart.com/getHistory.json?key=bb5776fcd3e1dd3c4ad7b7d691a0e83e&symbol=" 
	url += symbol
	url += "&type="
	url += data_type
	url += "&startDate="
	url += new_date
	# print url
	market_data = json.load(urllib2.urlopen(url))
	for data in market_data["results"]:
		result["open"]   = data["open"]
		result["high"]   = data["high"]
		result["low"]    = data["low"]
		result["close"]  = data["close"]
		result["volume"] = data["volume"]
		year 			 = int(data["tradingDay"].split("-")[0])
		month 			 = int(data["tradingDay"].split("-")[1])
		day 			 = int(data["tradingDay"].split("-")[2])
		date 			 = int(datetime.date(year,month,day).strftime("%s")) * 1000
		result["date"]	 = date
		results["values"].append(result)
		result = {}
	final_result.append(results)
	return final_result

def getStockSymbols():
	symbols = {}
	symbols["PowerShares QQQ Trust, Series 1"] = "QQQ"
	symbols["Facebook, Inc."] = "FB"
	# symbols["Apple Inc."] = "APPL"
	symbols["Netflix, Inc."] = "NFLX"
	symbols["Alphabet Inc Class A"] = "GOOGL"
	return symbols

def getMultipleSymbolHistory(symbols, data_type, date):
	final_result = []
	market_json = {}
	value = []
	values = []
	for symbol in symbols:
		market_json["key"] = symbol
		market_history = getMarketHistory(symbol, data_type, date)[0]["values"]
		# print market_history
		for i in range(0,len(market_history)):
			# pprint(market_history[i])
			value.append(market_history[i]["date"])
			value.append(market_history[i]["close"])
			values.append(value)
			value = []
		market_json["values"] = values
		values = []
		final_result.append(market_json)
		market_json = {}
	return final_result



# pprint(getMultipleSymbolHistory(["QQQ","FB","NFLX","GOOGL"],"daily","2016-11-14"))

