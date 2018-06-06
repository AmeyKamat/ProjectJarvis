import requests
import datetime
import configparser
import json

from circuits import Component, handler

from events.JobCompleteEvent import JobCompleteEvent

class TimeJobRunnerComponent(Component):

	config = configparser.ConfigParser()

	with open('./components/jobRunner/api_config.json', 'r') as apiConfig:	
		config = json.load(apiConfig)

	@handler("EntityPreprocessedEvent")
	def handleEntityPreprocessedEvent(self, context):
		if context.intent == 'time':
			self.handleTimeRequest(context)


	def handleTimeRequest(self, context):
		if "LOCATION" in context.entities:
			response = requests.get(self.config["GOOGLE_API"]["URL"]["GEOCODING"], params= {
				'address': context.entities["LOCATION"],
	    		'key': self.config["GOOGLE_API"]["KEY"]
			})

			latitude = response.json()["results"][0]["geometry"]["location"]["lat"]
			longitude = response.json()["results"][0]["geometry"]["location"]["lng"]
		else:
			response = requests.post(self.config["GOOGLE_API"]["URL"]["GEOLOCATION"], params= {
	    		'key': self.config["GOOGLE_API"]["KEY"]
			})
			latitude = response.json()["location"]["lat"]
			longitude = response.json()["location"]["lng"]
			print(response)

		print(response.json())
		
		

		response = requests.get(self.config["TIMEZONE_API"]["URL"]["GET_TIMEZONE"], params= {
			'key': self.config["TIMEZONE_API"]["KEY"],
			'format': 'json',
			'by': 'position',
			'lat': latitude,
			'lng': longitude
		})

		formattedResponse = response.json()
		print(formattedResponse)

		context.result['datetime'] = datetime.datetime.strptime(formattedResponse["formatted"], '%Y-%m-%d %H:%M:%S').strftime('%A, %d %B %Y , %I %M %p')
		context.result['location'] = context.entities['LOCATION'] if 'LOCATION' in context.entities else formattedResponse["zoneName"]
		self.fire(JobCompleteEvent(context)) 

	
