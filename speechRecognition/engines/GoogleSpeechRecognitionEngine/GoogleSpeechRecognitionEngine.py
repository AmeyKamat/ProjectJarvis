import speech_recognition as sr
from speechRecognition.speech_recognition_engine import SpeechRecognitionEngine;
from speechGeneration.speech_generator import SpeechGenerator

class GoogleSpeechRecognitionEngine(SpeechRecognitionEngine):
	def __init__(self):
		super().__init__()
		
	def listen(audio):
		print("connecting to google...")
		return sr.Recognizer().recognize_google(audio)

