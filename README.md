# OasisDashboard
This is a dashboard for visualizing big data related to smart grids. 

The dashboard has 5 areas of interest: 
Energy Data
Social Data
Weather Data
Market Data
Data Integration
The Energy Data area will show users AEE (Puerto Rico Electric Power Authority) historic data that was gathered from 2000 to 2015.

Social data is being gathered from Twitter. 
Tweets from Puerto Rico related to smart grids and energy are being streamed, stored and classified as positive or negative using a naïve bayes classifier. 
A pie chart shows the amount of positive and negative tweets. 
Two donut charts show the top 10 most positive and negative words and the tweets classified as positive or negative are being shown in near real-time. 
Positive tweets are colored blue and negative tweets are colored red. 
Twitter data may be exported as a csv file.

Weather data is being gathered using the Dark Sky API. 
This area shows the following weather data for a given town:

current condition
today’s forecast
today’s 12-hour forecast
4-day forecast
Users may search for a town by name or zip code. 
This area also shows users radar images for Puerto Rico. 
The hourly forecast for the next 24 hours can be exported as a csv file.
The Market data section will show users loads in MWhr and Day-ahead Locational Based Marginal Pricing gathered from the NYISO. 
Also, a graph comparing loads with Day-Ahead Locational Based Marginal Pricing (LBMP) is shown.

The Data Integration section is the area in the dashboard where users will be able to make comparisons between the different datasets. 
Users will be able to compare the following datasets:

Humidity data per hour for a given town
Precipitation data per hour for a given town
Wind data per hour for a given town
Temperature data per hour for a given town in Fahrenheit or Celsius
Load data
Load based marginal pricing data per zone
Positive Tweets
Negative Tweets
Up to four of these datasets may be compared. 
These datasets may be imported or exported.

# How to run 
To install the dashboard in Mac or Ubuntu, first the user must have installed Python in their computer. By default, MacOS and Ubuntu come with Python preinstalled so this should not be a problem. After this, the user must make sure that the following Python libraries are installed: Schedule, Forecastiopy, NLTK, Tweepy, Unidecode and Flask. To install each of these libraries, the users must first install pip, which can be done in Ubuntu by opening and typing in the terminal:
*sudo apt-get install python-setuptools python-dev build-essential*
*sudo easy_install pip*
For Mac users, open the terminal and type:
*curl https://bootstrap.pypa.io/ez_setup.py -o | sudo python *
*sudo easy_install pip*
With pip is installed, the user can proceed to install the necessary libraries by typing the following commands in the terminal:
*sudo pip install schedule
sudo pip install python-forecastio
sudo pip install nltk
sudo pip install unidecode
sudo pip install tweepy
sudo pip install flask*
After the user has finished typing all those commands, the user may now download the dashboard by going to the desired folder in the terminal where the dashboard will be stored. For example, the dashboard may be stored in /User/me/Desktop, where me is the name of the user of the computer. Assuming we want to store the dashboard in the Desktop in a folder called oasis_dashboard, we type the following in the terminal:
*cd 
cd Desktop/
mkdir oasis_dasboard
cd oasis_dashboard
git init
git clone https://github.com/alesanz237/oasis_dashboard.git
python startDashboard.py*
Once the user has finalized typing these commands in the terminal, the dashboard should be successfully installed. To verify that the dashboard is running, the terminal should show say that the dashboard is running on port 5000. If everything was installed successfully, the user may go the web browser and type in the url localhost:5000 to use the dashboard. 

The OASIS dashboard is an open source project and is part of the OASIS project, more information about this project is provided in oasis.uprm.edu
