# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
"""
    Programmer: Alejandro Sánchez
    Script that gathers weather data from NOAA of the 78 municipalities of Puerto Rico 
"""
from params import lat_long_locations
import json
import urllib2
# import requests  # For getting data from a webpage
# from lxml import html # For reading content from a webpage

def getWeather():
    """ Funtion that gathers the weather data from Puerto Rico"""
    for i in range(0,len(lat_long_locations)-1):
 		if i%2 == 0:
 			lat = lat_long_locations[i]
 			lon = lat_long_locations[i+1]
			url = "http://forecast.weather.gov/MapClick.php?lat=" + str(lat) + "&lon=" + str(lon) + "&FcstType=json"
			data = json.load(urllib2.urlopen(url))
			print data
 		else:
			continue

if __name__ == '__main__':
    getWeather()