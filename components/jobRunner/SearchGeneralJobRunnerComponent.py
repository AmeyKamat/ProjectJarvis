import requests
import datetime
import configparser
import json

from circuits import Component, handler

from events.JobCompleteEvent import JobCompleteEvent
from events.EntityPreprocessedEvent import EntityPreprocessedEvent

class SearchGeneralJobRunnerComponent(Component):

	config = configparser.ConfigParser()

	with open('./components/jobRunner/api_config.json', 'r') as apiConfig:	
		config = json.load(apiConfig)

	@handler("EntityPreprocessedEvent")
	def handleEntityPreprocessedEvent(self, context):
		if context.intent == 'search-general':
			self.handleSearchGeneralRequest(context)


	def handleSearchGeneralRequest(self, context):
		if "QUERY" in context.entities:
			searchQuery = context.entities["QUERY"]
		else:
			searchQuery = context.message
		result = {}
		result["url"] = self.config["GOOGLE_API"]["URL"]["SEARCH"] + searchQuery
		context.result =  result
		self.fire(JobCompleteEvent(context)) 

	
