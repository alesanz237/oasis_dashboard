# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template, request, send_from_directory
import os.path, sys, subprocess, time
sys.path.insert(0, "./code")
from helper import getKey1, getKey2, getAEEData
from sentimentAnalysis import getTweetsLen, getPositiveWords, getNegativeWords, getTweets
from weather import getTodaysWeather, getHourlyWeather, getDailyWeather, convertZipcodeToTown, getCorrectTownName, getHourlyWeatherInCSV
from market import getDataForLBMPZonalComparison, getDataForLoadComparisons, getDataForLBMPvsLoadComparisons

app = Flask("__OasisDashboard__")

@app.route("/")
def init():
    return render_template("index.html")

@app.route("/dashboard")
def init1():
    return render_template("index.html")

@app.route("/energy")
def getEnergy():
    return render_template("energy.html")

@app.route("/market")
def getMarket():
    return render_template("market.html")

@app.route('/_getAEEDATA')
def get_AEEData():
    key_1 =  request.args['key_1']
    aee_data = getAEEData(key_1)
    return jsonify(result=aee_data)

@app.route('/_getLBMPData')
def get_LBMPData():
    lbmpData = getDataForLBMPZonalComparison()
    return jsonify(result=lbmpData)

@app.route('/_getLoadData')
def get_LoadData():
    load_data = getDataForLoadComparisons()
    return jsonify(result=load_data)

@app.route('/_getLBMPvsLoadData')
def get_LBMPvsLoadData():
    lbmp_vs_load_data = getDataForLBMPvsLoadComparisons()
    return jsonify(result=lbmp_vs_load_data)

@app.route("/twitter")
def getTwitter():
    return render_template("twitter.html")

@app.route('/_getTweetsCount')
def get_TweetsCount():
    tweets_len = []
    for length in getTweetsLen():
        tweets_len.append(length)
    print tweets_len
    return jsonify(result=tweets_len)

@app.route('/_getPositiveWords')
def get_PositiveWords():
    return jsonify(result=getPositiveWords())

@app.route('/_getNegativeWords')
def get_NegativeWords():
    return jsonify(result=getNegativeWords())

@app.route('/_getTweets')
def get_Tweets():
    return jsonify(result=getTweets())

@app.route("/weather")
def getWeather():
    return render_template("weather.html")

@app.route("/_getWeatherData")
def getWeatherData():
    temp = str(request.args['temp'])
    town = unicode(request.args['town'])
    weather = {}
    # print type(town)
    todaysForecast = getTodaysWeather(town, temp)
    hourlyForecast = getHourlyWeather(town, temp)
    dailyForecast  = getDailyWeather(town, temp)
    weather["todaysForecast"] = todaysForecast
    weather["hourlyForecast"] = hourlyForecast
    weather["dailyForecast"] = dailyForecast
    print weather 
    return jsonify(result=weather)

@app.route('/returnTweets')
def return_tweets():
    date = time.strftime("%d-%m-%Y")
    filename = "tweets_"+date+".csv"
    return send_from_directory(directory='data/tweets',filename=filename, as_attachment=True)

@app.route('/returnWeather')
def return_weather():
    temp = str(request.args['temp'])
    town = unicode(request.args['town'])
    print temp, town
    getHourlyWeatherInCSV(town, temp)
    if town[0] == "0":
        town = convertZipcodeToTown(town)
    town = getCorrectTownName(town)
    filename = town+"_"+temp+".csv"
    print filename
    return send_from_directory(directory='data/weather',filename=filename, as_attachment=True)

@app.route('/returnLoads')
def return_loads():
    return send_file('/var/www/PythonProgramming/PythonProgramming/static/images/python.jpg', attachment_filename='python.jpg')

if __name__ == "__main__":
    process = subprocess.Popen('static/start/twitterStreamer.sh',shell=True)
    app.run(host='0.0.0.0')
    app.run()
    process.kill()
