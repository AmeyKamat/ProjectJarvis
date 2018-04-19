from circuits import Component, handler

from events.DialogReadyEvent import DialogReadyEvent

class DialogGeneratorComponent(Component):

	@handler("IntentConfidenceCheckFailedEvent")
	def handleIntentConfidenceCheckFailedEvent(self):
		self.fire(DialogReadyEvent("I did not understand what you just said"))

	@handler("EntityIncompleteEvent")
	def handleEntityIncompleteEvent(self, intent, incompleteEntities):
		self.fire(DialogReadyEvent("I need more information about" + str(incompleteEntities)))

	@handler("JobStartedEvent")
	def handleJobStartedEvent(self, message):
		self.fire(DialogReadyEvent(message))	

	@handler("JobCompleteEvent")
	def handleJobCompleteEvent(self, message):
		self.fire(DialogReadyEvent(message))

