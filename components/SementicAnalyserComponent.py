from circuits import Component, handler

from events.MessageAnalysedEvent import MessageAnalysedEvent
from sementicAnalysis.SementicAnalyser import SementicAnalyser

class SementicAnalyserComponent(Component):

	sementicAnalyser = SementicAnalyser()

	@handler("MessageReceivedEvent")
	def handleMessageReceivedEvent(self, request):
		request.intent, request.confidence, request.entities = self.sementicAnalyser.analyse(request.message)
		self.fire(MessageAnalysedEvent(request))

