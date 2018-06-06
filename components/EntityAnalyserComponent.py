from circuits import Component, handler

from events.EntityIncompleteEvent import EntityIncompleteEvent
from events.EntityAnalysedEvent import EntityAnalysedEvent

class EntityAnalyserComponent(Component):

	
	@handler("ContextBuiltEvent")
	def handleContextBuiltEvent(self, context):
		self.fire(EntityAnalysedEvent(context))




