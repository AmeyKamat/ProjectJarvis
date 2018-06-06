from circuits import Component, handler

from events.EntityPreprocessedEvent import EntityPreprocessedEvent

class EntityPreprocessorComponent(Component):

	
	@handler("EntityAnalysedEvent")
	def handleEntityAnalysedEvent(self, context):
		self.fire(EntityPreprocessedEvent(context))

