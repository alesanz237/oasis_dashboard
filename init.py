# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template, request
from helper import getWeatherFromOWM, getWeatherFromNOAA, getPRTweets, getKey1, getKey2, getAEEData, getStockSymbols, getMarketHistory
from sentimentAnalysis import getTweetsLen, getPositiveWords, getNegativeWords, getTweets
import subprocess
app = Flask(__name__)

@app.route('/_weather_data')
def get_weather():
    town =  request.args['town']
    # print town
    weather_from_owm = []
    # weather_from_owm.append(getWeatherFromOWM("Cayey"))
    # print getWeatherFromOWM(town)
    return jsonify(getWeatherFromOWM(town))

@app.route('/_twitter_data')
def get_twitterData():
    town =  request.args['town']
    pr_tweets = getPRTweets(town)
    return jsonify(pr_tweets)

@app.route("/")
def init():
    return render_template("index.html")

@app.route("/dashboard")
def init1():
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

@app.route("/market")
def getMarket():
    keys = sorted(getKey1())
    symbols = getStockSymbols()
    print symbols
    return render_template("market.html",keys=keys, symbols=symbols)

@app.route('/_getAEEDATA')
def get_AEEData():
    key_1 =  request.args['key_1']
    aee_data = getAEEData(key_1)
    return jsonify(result=aee_data)

@app.route('/_getMarketHistoryData')
def get_MarketHistoryData():
    symbol =  str(request.args['symbol'])
    dType =  str(request.args['type'])
    startDate = str(request.args['startDate'])
    market_history = getMarketHistory(symbol,dType,startDate)
    return jsonify(result=market_history)

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

@app.route("/map")
def getMap():
    return render_template("map.html")

if __name__ == "__main__":
    subprocess.Popen('static/start/twitterStreamer.sh',shell=True)
    app.run()