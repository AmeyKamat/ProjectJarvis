from circuits import Component, handler

from events.MessageAnalysedEvent import MessageAnalysedEvent

class SementicAnalyserComponent(Component):

	@handler("MessageReceivedEvent")
	def handleMessageReceivedEvent(self, message):
		print("started")
		if message == "where is mumbai":
			self.fire(MessageAnalysedEvent("location", 0.967, {"LOCATION": "mumbai"}))
		elif message == "sleep":
			self.fire(MessageAnalysedEvent("shut-down", 0.732, {}))
		elif message == "where is pune":
			self.fire(MessageAnalysedEvent("location", 0.932, {}))

