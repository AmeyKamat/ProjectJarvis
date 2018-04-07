import pyttsx3;

class SpeechGenerator(object):

	def __init__(self):
		super(SpeechGenerator, self).__init__();
		self.engine = pyttsx3.init()
		self.engine.setProperty('voice', "+f3");
		self.engine.setProperty('rate', 160)

	def speak(self, text):
		print(text);
		self.engine.say(text);
		self.engine.runAndWait()