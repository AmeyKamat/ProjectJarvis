from circuits import Component, handler

from events.JobCompleteEvent import JobCompleteEvent

class ComplimentJobRunnerComponent(Component):

	@handler("EntityPreprocessedEvent")
	def handleEntityPreprocessedEvent(self, context):
		if context.intent == 'compliment':
			self.handleComplimentRequest(context)


	def handleComplimentRequest(self, context):
		self.fire(JobCompleteEvent(context)) 

	
