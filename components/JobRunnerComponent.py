from circuits import Component, handler

from events.JobStartedEvent import JobStartedEvent
from events.JobCompleteEvent import JobCompleteEvent

class JobRunnerComponent(Component):

	
	@handler("EntityPreprocessedEvent")
	def handleEntityPreprocessedEvent(self, intent, entities):
		#do something for very long time
		self.fire(JobCompleteEvent('Intent: ' + intent + " Entities: " + str(entities)))
