import pyttsx3
from time import sleep

engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', 'ru') 
engine.setProperty('voice', voices[2].id) 
engine.setProperty("rate", 210)

#sleep(1)
engine.say("Леха привет, я твой робот")

#engine.say(str(text))

engine.runAndWait()