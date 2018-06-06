from circuits import Component, handler

from events.IntentConfidenceCheckFailedEvent import IntentConfidenceCheckFailedEvent
from events.ContextBuiltEvent import ContextBuiltEvent
from context.Context import Context

class ContextBuilderComponent(Component):

	contextStack = []

	@handler("MessageAnalysedEvent")
	def handleMessageAnalysedEvent(self, context):
		if context.confidence>0.8:
			self.contextStack.append(context)
			print("Context created: " + str(self.contextStack[-1]))
			self.fire(ContextBuiltEvent(context))
		else:
			self.fire(IntentConfidenceCheckFailedEvent(context))