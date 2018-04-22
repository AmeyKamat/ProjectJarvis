from circuits import Component, handler

from events.MessageAnalysedEvent import MessageAnalysedEvent
from sementicAnalysis.SementicAnalyser import SementicAnalyser

class SementicAnalyserComponent(Component):

	sementicAnalyser = SementicAnalyser()

	@handler("MessageReceivedEvent")
	def handleMessageReceivedEvent(self, message):
		intent, confidence, entities = self.sementicAnalyser.analyse(message)
		self.fire(MessageAnalysedEvent(intent, confidence, entities))

