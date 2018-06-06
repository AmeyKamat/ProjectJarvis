import random
import configparser
import json
import re

from num2words import num2words

from circuits import Component, handler

from events.DialogReadyEvent import DialogReadyEvent

class DialogGeneratorComponent(Component):

	dialogues = configparser.ConfigParser()

	with open('./resources/dialogues.json', 'r') as dialogueConfig:	
		dialogues = json.load(dialogueConfig)

	@handler("IntentConfidenceCheckFailedEvent")
	def handleIntentConfidenceCheckFailedEvent(self, context):
		context.dialogue = self.dialogues["unknown"][random.randint(0, len(self.dialogues["unknown"])-1)]["message"]
		self.fire(DialogReadyEvent(context))

	@handler("EntityIncompleteEvent")
	def handleEntityIncompleteEvent(self, context):
		self.fire(DialogReadyEvent("I need more information"))	

	@handler("JobCompleteEvent")
	def handleJobCompleteEvent(self, context):
		intent = context.intent
		print(context.result)
		if intent in ['time', 'greet', 'compliment', 'question', 'search-general']:
			message = self.dialogues[intent][random.randint(0, len(self.dialogues[intent])-1)];
			generatedMessage = message["message"]
			for parameter in message["parameters"]:
				generatedMessage = generatedMessage.replace('{}', context.result[parameter], 1)
		else:
			generatedMessage = intent

		context.dialogue = self.scrubForSpeech(generatedMessage)
		self.fire(DialogReadyEvent(context))

	def scrubForSpeech(self, text):
		formattedText = text
		# for word in re.split(r'(\d+)', text):
		# 	if word.isdigit():
		# 		formattedText = formattedText + num2words(int(word))
		# 	else:
		# 		formattedText = formattedText + word
		return formattedText

