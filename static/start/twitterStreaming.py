#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time

import sys
import time

energy_words_english = ["absorb","AC","accumulator","alternating current","anthracite coal","appliance","battery","biodiesel","biofuel","biomass","bituminous coal","blackout","boiler","British thermal unit","Btu","capacity","carbon","carbon footprint","carbon tax","charcoal","chemical energy","clean energy","climate change","coal","coke","combustion","conservation","crude oil","current","dam","DC","diesel","direct current","drill","dynamo","efficiency","efficient","electric","electrical","electrical grid","electromagnetic energy","electron","energy","engine","engineer","entropy","environment","erg","ethanol","fossil fuel","flexible fuel","flywheel","fuel","fuel cell","furnace","gas","gasoline","gas-turbine","generate","generation","generator","geothermal","global warming","green","green energy","greenhouse effect","greenhouse gas","grid","heat","heat exchange","high-voltage","horsepower","human-powered","hybrid","hydrocarbon","hydroelectric","hydrogen","hydrothermal","industry","internal combustion engine","inverter","jet fuel","joule","Kelvin scale","kilowatt","kilowatt-hour","kinetic energy","light","liquefied petroleum gas","magnetic energy","megawatt","methane","methanol","mining","motor","natural gas","nuclear","nuclear energy","nuclear power","nuclear reactor","nucleus","off-the-grid","oil","oil rig","peak oil","peat","petroleum","photon","photovoltaic","photovoltaic panel","pollution","potential energy","power","power grid","power lines","power plant","power station","power transmission","propane","public utility","radiant","radiate","reactor","reciprocating engine","reflect","renewable","reservoir","shale","solar panel","solar power","static electricity","steam","steam engine","steam turbine","sun","sunlight","sunshine","sustainable","temperature","therm","thermal energy","thermodynamics","tidal power","transmission lines","transmit","turbine","utilities","volt","waste","watt","wattage","wave power","wind","wind farm","windmill","wind power","wind turbine","work"]

energy_words_spanish = ["absorber","acumulador","corriente alterna",u"carbón","aparato",u"batería","Biodiesel","Biocombustible","Biomasa",u"carbón bituminoso",u"apagón","caldera",u"Unidad Térmica Británica","BTU","capacidad",u"carbón","Huella de carbono","impuesto sobre el carbono",u"carbón",u"energía química",u"energia limpia",u"energía",u"cambio climático",u"carbón","coca",u"combustión",u"conservación",u"petróleo crudo","corriente","presa","corriente continua","diesel","corriente continua","perforar","dinamo","eficiencia","eficiente",u"eléctrico",u"eléctrico",u"red eléctrica",u"energía electromagnética",u"electrón",u"energía","motor","ingeniero",u"Entropía","ambiente","ergio","etanol","combustible fosil","Combustible flexible","volante","gasolina","pila de combustible","horno","gas","gasolina","turbina de gas","generar","Generacion","generador",u"Geotérmica","calentamiento global","verde",u"energía verde","efecto invernadero","gases de efecto invernadero",u"cuadrícula","calor","de intercambio de calor","Alto voltaje","caballo de fuerza"]

#Variables that contains the user credentials to access Twitter API 
access_token = "364565294-CqGNORYeBoSajSaiCRXVjTjf1AzZHEV2iYnBR1xQ"
access_token_secret = "zhtGWT1etNPVc3xWGBbRR8xf0gaGBGvOuk2gN4TbrIKVe"
consumer_key = "7BcsxgQByiwwdgIhCuO6VuOLg"
consumer_secret = "iZH0eeEeX4pb69jAxspk0tvo4o54nRE4hdwWHWrt4Ss8RliBqD"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

	def __init__(self):
		self.num_tweets = 0

	def on_data(self, data):
		# if (time.time() - self.start_time) < self.limit:
		if self.num_tweets < 5000:
			print data
			self.num_tweets+=1
			return True
		return False

	def on_error(self, status):
		print status			


if __name__ == '__main__':

	#This handles Twitter authetification and the connection to Twitter Streaming API
	start_time = time.time()
	l = StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	stream = Stream(auth, l)

	#This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
	if (sys.argv[1] == 's'):
		stream.filter(track=energy_words_spanish)
	else:
		stream.filter(track=energy_words_english)




