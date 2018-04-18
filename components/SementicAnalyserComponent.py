from circuits import Component, handler

from events.MessageAnalysedEvent import MessageAnalysedEvent

class SementicAnalyserComponent(Component):

	@handler("MessageReceivedEvent")
	def handleMessageReceivedEvent(self, message):
		print("started")
		if message == "where is mumbai":
			self.fire(MessageAnalysedEvent("self-location", 0.967, {"LOCATION": "mumbai"}))
		elif message == "sleep":
			self.fire(MessageAnalysedEvent("self-location", 0.732, {}))

