import requests
import datetime
import configparser
import json
import copy

from circuits import Component, handler

from events.JobCompleteEvent import JobCompleteEvent
from events.EntityPreprocessedEvent import EntityPreprocessedEvent

class QuestionJobRunnerComponent(Component):

	config = configparser.ConfigParser()

	with open('./components/jobRunner/api_config.json', 'r') as apiConfig:	
		config = json.load(apiConfig)

	@handler("EntityPreprocessedEvent")
	def handleEntityPreprocessedEvent(self, context):
		if context.intent == 'question':
			self.handleQuestionRequest(context)


	def handleQuestionRequest(self, context):
		response = requests.get(self.config["DUCKDUCKGO_API"]["URL"]["QUESTION"], params= {
			'q': context.message,
			'format': 'json'
		})
		formattedResponse = response.json()
		if formattedResponse["Answer"] != "":
		 	context.result["answer"] = formattedResponse["Answer"]
		 	context.result["source"] = "DuckDuckGo"
		elif formattedResponse["Definition"] != "":
		 	context.result["answer"] = formattedResponse["Definition"]
		 	context.result["source"] = formattedResponse["DefinitionSource"]
		elif formattedResponse["AbstractText"] != "":
		 	context.result["answer"] = formattedResponse["AbstractText"]
		 	context.result["source"] = formattedResponse["AbstractSource"]
		else:
			context.intent = 'search-general'
			self.fire(EntityPreprocessedEvent(context))

		if context.intent == 'question':
			self.fire(JobCompleteEvent(copy.deepcopy(context))) 

	
