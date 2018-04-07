from speechRecognition.speech_recognition_engine_loader import SpeechRecognitionEngineLoader;
from speechGeneration.speech_generator import SpeechGenerator

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr

class SpeechRecognizer(object):

    sg = SpeechGenerator();
    speechRecognitionEngines = [];
    
    def __init__(self, available_engines):
        self.sg.speak("Loading Available Speech Recognition Engines.")
        for engineName in available_engines:
            self.speechRecognitionEngines.append(SpeechRecognitionEngineLoader().loadEngine(engineName));

    def listen(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.sg.speak("Adjusting Microphone for noise.")
            r.adjust_for_ambient_noise(source)
            self.sg.speak("Ready.")
            print("Say something!")
            audio = r.listen(source)
            for speechRecognitionEngine in self.speechRecognitionEngines:
                try:
                    text = speechRecognitionEngine.listen(audio);
                    self.sg.speak("You said: " + text)
                    return text;
                except Exception as e:
                    print(e)
                    continue;
            self.sg.speak("Pardon?")
            raise ValueError("Voice could not be identified");

