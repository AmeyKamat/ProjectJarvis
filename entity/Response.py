class Response(object):
	message = None
	intent = None
	confidence = 0
	entities = {}
	result = {}

	def __init__(self, message):
		self.message = message
