from circuits import Component, handler

from events.JobStartedEvent import JobStartedEvent
from events.JobCompleteEvent import JobCompleteEvent

class JobRunnerComponent(Component):

	
	@handler("EntityPreprocessedEvent")
	def handleEntityPreprocessedEvent(self, intent, entities):
		self.fire(JobStartedEvent("job started"))
		#do something for very long time
		for i in range(1000000000):
			pass
		self.fire(JobCompleteEvent("job complete"))
