
class Context(object):

	message = None
	intent = None
	incompleteEntities = [] 
	confidence = 0
	entities = {}
	result = {}
	dialogue = None
	status = "INITIALISED"

	def __init__(self, message):
		self.message = message
