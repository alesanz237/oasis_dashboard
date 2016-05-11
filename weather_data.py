# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
import pyowm # Python wrapper for OpenwWeatherMap
from params import lat_lon_towns
owm = pyowm.OWM('17e7fa6633e1d589da7ab67277d42774') # API Key for OpenWeatherMap API

def getLatLonByTown(town_name):
	""" Function that returns the coordinates of a town, given its name """
	int_coords = []
	for town in lat_lon_towns:
		if town_name == town:
			coordinates = lat_lon_towns[town_name].split(",",1)
	for coor in coordinates:
		int_coords.append(float(coor))
	# print int_coords, "\n\n"
	return int_coords

def getWeatherFromOWM(town):
	""" Getting weather information by location from the Open Weather Map API """

	coors = getLatLonByTown(town) # Getting town coordinates

	# Getting weather data and storing it in a dictionary
	weather = owm.weather_at_coords(coors[0],coors[1]).get_weather()
	weather_data = {}
	weather_data["cloud_coverage"] = str(weather.get_clouds()) + "%" # Cloud Coverage
	weather_data["rain"]    	   = weather.get_rain()				   	   				  # Rain Volume
	weather_data["wind"] 		   = weather.get_wind()		   			   			  	  # Wind degree and speed
	weather_data["humidity"]  	   = str(weather.get_humidity()) + "%" 	  # Humidity percentage
	# weather_data["pressure"] 	   = weather.get_pressure()				   				  # Get Atmospheric pressure
	weather_data["temperature"]    = weather.get_temperature('fahrenheit') 				  # Get temperature
	weather_data["status"] 		   = weather.get_detailed_status()           # Get weather status

	# Parsing wind data
	speed = "" # String contianing the speed of the weather
	direction = "" # String containing the direction of the wind
	for key,value in weather_data["wind"].iteritems():
		if key == "speed":
			speed = str(value) +  " m/s"
		if key == "deg":
			if value == 0 or value == 360:
				direction = " north"
			elif value > 0 and value <= 90:
				direction = " northeast"
			elif value == 90:
				direction = " east"
			elif value > 90 and value <= 180:
				direction = " southeast"
			elif value == 180:
				direction = " south"
			elif value > 180 and value <= 270:
				direction = " southwest"
			elif value == 270:
				direction = " west"
			else:
				direction = " northwest"
	weather_data["wind"] = speed + direction

	# Parsing temperature data:
	weather_data["temperature"] = str(weather_data["temperature"]["temp"])

	# Parsing rain data
	weather_data["rain"] = "Rain volume in the last three hours: " + str(weather_data["rain"]['3h']) if weather_data["rain"] else "No rain activy in the last three hours"

	return weather_data

print getWeatherFromOWM("Ponce")