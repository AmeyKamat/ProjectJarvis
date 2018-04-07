import speech_recognition as sr
from speechRecognition.speech_recognition_engine import SpeechRecognitionEngine;
from speechGeneration.speech_generator import SpeechGenerator

class SphinxSpeechRecognitionEngine(SpeechRecognitionEngine):
	def __init__(self):
		super().__init__()
		
	def listen(audio):
		print("falling back to sphinx...")
		return sr.Recognizer().recognize_sphinx(audio)

