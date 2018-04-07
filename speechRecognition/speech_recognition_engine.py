class SpeechRecognitionEngine(object):
	
	def __init__(self):
		super(SpeechRecognitionEngine, self).__init__()

	def listen(self, audio):
		raise NotImplementedError("This method needs to be implemented");
		