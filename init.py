from flask import Flask, render_template, request
from helper import getWeatherFromOWM, getWeatherFromNOAA
app = Flask(__name__)

@app.route("/")
def init():
    return render_template("index.html")

@app.route('/town_info',methods=["Get"])
def townInfo():
    town =  request.args['town']
    # svg_path = request.args['svg_path']
    # print(svg_path)
    # LLamar el codigo de Weather y Twitter

    # Getting weather data from Open WeatherMap API
    weather_from_owm = []
    weather_from_owm.append(getWeatherFromOWM(town))

    # Getting weather data from NOAA
    # weather_from_noaa = []
    # forecast = getWeatherFromNOAA(town)[0]
    # observation = getWeatherFromNOAA(town)[1]
    # weather_from_noaa.append(forecast)
    # current_observation = []
    # current_observation.append(observation)
    

    # print weather
    # return render_template("town_info.html", town=town, weatherOWM=weather_from_owm, weatherNOAA=weather_from_noaa, current_weather=current_observation)
    return render_template("town_info.html", town=town, weatherOWM=weather_from_owm)

@app.route("/energy")
def getEnergy():
    return render_template("energy.html")

@app.route("/twitter")
def getTwitter():
    return render_template("twitter.html")

@app.route("/weather")
def getWeather():
    return render_template("weather.html")

@app.route("/map")
def getMap():
    return render_template("map.html")

if __name__ == "__main__":
	app.run()