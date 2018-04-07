#!/usr/bin/env python3

from speechRecognition.speech_recognizer import SpeechRecognizer

speechRecognizer = SpeechRecognizer(['GoogleSpeechRecognitionEngine', 'SphinxSpeechRecognitionEngine']);
print(speechRecognizer.listen());