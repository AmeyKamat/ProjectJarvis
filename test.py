import pyttsx3;
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for i in range(100):
   engine.setProperty('voice', "en+f"+str(i));
   engine.setProperty('rate', 160)
   voice = engine.getProperty("voice")
   engine.say("I am {0}".format(i))
   engine.say("Do you want tea sir?")
engine.runAndWait()