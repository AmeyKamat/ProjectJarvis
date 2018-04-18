
class Context(object):

	intent = None
	entities = []
	status = None
	
	def __init__(self, intent, entities, status="INITIALISED"):
		super(Context, self).__init__()
		self.intent = intent
		self.entities = entities
		self.status = status
		