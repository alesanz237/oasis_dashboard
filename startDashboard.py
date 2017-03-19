# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template, request, send_from_directory
import os.path, sys, subprocess, time, csv
sys.path.insert(0, "./code")
from dataGathering import DataGathering
from dataIntegration import DataIntegration
from helper import Helper
from sentimentAnalysis import getTweetsLen, getPositiveWords, getNegativeWords, getTweets

app = Flask("__OasisDashboard__")

data             = DataGathering()   # Class that returns data that will be displayed in the dashboard
helper           = Helper()          # Class that has helper functions for the dashboar
data_integration = DataIntegration() # Class that returns integrated data for home section
# twitter_streaming_process = subprocess.Popen('code/processes/twitterStreamer.sh',shell=True)

@app.route("/")
def init():
    data_integration.setSelectValues()
    return render_template("home.html",select_values=data_integration.getSelectValues(0))

@app.route("/home")
def init1():
    data_integration.setSelectValues()
    return render_template("home.html",select_values=data_integration.getSelectValues(0))

@app.route("/energy")
def getEnergy():
    return render_template("energy.html")

@app.route("/market")
def getMarket():
    return render_template("market.html")

@app.route("/twitter")
def getTwitter():
    return render_template("twitter.html")

@app.route("/weather")
def getWeather():
    return render_template("weather.html")

@app.route('/_getAEEDATA')
def get_AEEData():
    """ 
        Route that returns the AEE data that will be displayed
        in the dashboard
    """
    key = request.args['key_1']
    return jsonify(result = data.getAEEData(key))

@app.route('/_getLBMPData')
def get_LBMPData():
    """ 
        Route that returns the LBMP data that will be displayed
        in the dashboard
    """
    return jsonify(result = data.getDataForLBMPZonalComparison())

@app.route('/_getLoadData')
def get_LoadData():
    """ 
        Route that returns the load data that will be displayed
        in the dashboard
    """
    return jsonify(result = data.getDataForLoadComparisons())

@app.route('/_getLBMPvsLoadData')
def get_LBMPvsLoadData():
    """ 
        Route that returns the lbmp vs load data that 
        will be displayed in the dashboard
    """
    return jsonify(result = data.getDataForLBMPvsLoadComparisons())

@app.route('/_getTweetsCount')
def get_TweetsCount():
    """ 
        Route that returns the tweets count data
        that will be displayed in the dashboard
    """
    return jsonify(result=getTweetsLen())

@app.route('/_getPositiveWords')
def get_PositiveWords():
    """ 
        Route that returns the top 10 words in
        positive tweets that will be displayed
        in the dashboard
    """
    return jsonify(result=getPositiveWords())

@app.route('/_getNegativeWords')
def get_NegativeWords():
    """ 
        Route that returns the top 10 words in
        negative tweets that will be displayed
        in the dashboard
    """
    return jsonify(result=getNegativeWords())

@app.route('/_getTweets')
def get_Tweets():
    """ 
        Route that returns classified tweets
        that will be displayed in the dashboard
    """
    return jsonify(result=getTweets())

@app.route("/_getWeatherData")
def getWeatherData():
    """ 
        Route that returns the weather data that will be displayed
        in the dashboard
    """
    temp    = str(request.args['temp'])
    town    = unicode(request.args['town'])
    weather = {}
    todaysForecast = data.getTodaysWeather(town, temp)
    hourlyForecast = data.getHourlyWeather(town, temp, 13)
    dailyForecast  = data.getDailyWeather(town, temp)
    weather["todaysForecast"] = todaysForecast
    weather["hourlyForecast"] = hourlyForecast
    weather["dailyForecast"]  = dailyForecast
    return jsonify(result = weather)

@app.route("/_updateSelectValues")
def updateSelectValues():
    """ 
        Route that updates the select values and
        returns the select values for the home section
    """
    selected_value = str(request.args['selected_value'])
    select         = request.args['select']
    data_integration.updateSelectValues(select, selected_value)
    return jsonify(result = data_integration.getSelectValues(select))

@app.route("/_getTowns")
def getTowns():
    """ 
        Route that updates the select values and
        returns the select values for the home section
    """    
    return jsonify(result = helper.getTowns())

@app.route("/_getZones")
def getZones():
    """ 
        Route that updates the select values and
        returns the select values for the home section
    """    
    return jsonify(result = helper.getZones())

@app.route("/_resetSelectValues")
def resetSelectValues():
    """ 
        Route that updates the select values and
        returns the select values for the home section
    """
    data_integration.setSelectValues()
    return jsonify(result = data_integration.getSelectValues(0))

@app.route("/_getIntegrationDataset")
def getIntegrationDataset():
    """ 
        Route that updates the select values and
        returns the select values for the home section
    """
    dataset = request.args.getlist('data[]')
    # print dataset
    data_integration.addData(dataset)
    print data_integration.getDataset()
    return jsonify(result = data_integration.getDataset())

@app.route('/returnTweets')
def return_tweets():
    """ 
        Route that returns the twitter data in a csv file to be downloaded
    """
    return send_from_directory(directory='data/tweets',filename="tweets.csv", as_attachment=True)

@app.route('/returnWeather')
def return_weather():
    """ 
        Route that returns the weather data in a csv file to be downloaded
    """
    temp = str(request.args['temp'])
    town = unicode(request.args['town'])
    if town[0] == "0":
        town = helper.convertZipcodeToTown(town)
    filename = town+"_"+temp+".csv"
    return send_from_directory(directory='data/weather',filename=filename, as_attachment=True)

@app.route('/returnLoads')
def return_loads():
    """ 
        Route that returns the load data in a csv file to be downloaded
    """
    url = 'http://mis.nyiso.com/public/dss/nyiso_loads.csv'
    response = urllib2.urlopen(url)
    load_data = csv.reader(response)
    return send_file(load_data, attachment_filename='nyiso_loads.csv')

if __name__ == "__main__":
    # Starting process that streams twitter data and classifies it as positive or negative
    twitter_streaming_process = subprocess.Popen('code/processes/twitterStreamer.sh',shell=True)
    weather_gathering_process = subprocess.Popen('code/processes/generateWeatherData.sh',shell=True)

    # Starting server
    app.run(host='0.0.0.0')

    twitter_streaming_process.kill()
    