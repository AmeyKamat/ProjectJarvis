from circuits import Component, handler

from events.JobCompleteEvent import JobCompleteEvent

class GreetJobRunnerComponent(Component):

	@handler("EntityPreprocessedEvent")
	def handleEntityPreprocessedEvent(self, context):
		if context.intent == 'greet':
			self.handleGreetRequest(context)


	def handleGreetRequest(self, context):
		self.fire(JobCompleteEvent(context)) 

	
