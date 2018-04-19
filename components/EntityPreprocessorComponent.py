from circuits import Component, handler

from events.EntityPreprocessedEvent import EntityPreprocessedEvent

class EntityPreprocessorComponent(Component):

	
	@handler("EntityAnalysedEvent")
	def handleEntityAnalysedEvent(self, intent, entities):
		self.fire(EntityPreprocessedEvent(intent, entities))

