from circuits import Component, handler

from events.IntentConfidenceCheckFailedEvent import IntentConfidenceCheckFailedEvent
from events.ContextBuiltEvent import ContextBuiltEvent
from context.Context import Context

class ContextBuilderComponent(Component):

	contextStack = []

	@handler("MessageAnalysedEvent")
	def MessageReceivedEvent(self, intent, confidence, entities):
		if confidence>0.8:
			self.contextStack.append(Context(intent, entities))
			self.fire(ContextBuiltEvent(intent, entities))
		else:
			self.fire(IntentConfidenceCheckFailedEvent())



