import importlib
from speechRecognition.speech_recognition_engine import SpeechRecognitionEngine;

class SpeechRecognitionEngineLoader(object):

	def __init__(self):
		super(SpeechRecognitionEngineLoader, self).__init__()
		
	def loadEngine(self, engineName):
		print(engineName);
		module = importlib.import_module('speechRecognition.engines.{0}.{1}'.format(engineName, engineName));
		module = getattr(module, engineName);
		if issubclass(module, SpeechRecognitionEngine):
			return module;
		else:
			raise ValueError("failed to load {0} engine".format(engineName));
