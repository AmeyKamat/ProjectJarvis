from circuits import Component, handler

from events.EntityIncompleteEvent import EntityIncompleteEvent
from events.EntityAnalysedEvent import EntityAnalysedEvent

class EntityAnalyserComponent(Component):

	
	@handler("ContextBuiltEvent")
	def handleContextBuiltEvent(self, intent, entities):
		if intent == "location":
			if "LOCATION" not in entities:
				self.fire(EntityIncompleteEvent(intent, ["LOCATION"]))
			else:
				self.fire(EntityAnalysedEvent(intent, entities))




