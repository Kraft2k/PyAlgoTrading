import speech_recognition as sr
import pyttsx3
from time import sleep

engine = pyttsx3.init()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ввод >>")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source,duration = 1)
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio,language='ru-ru')
            print(text)
        except: 
            text = listen()
        return text

voices = engine.getProperty('voices')
engine.setProperty('voice', '') 
#engine.setProperty('voice', voices[2].id) 
engine.setProperty("rate", 210)
i = 0
for voice in voices:
    print(voice.name)
    if voice.name == 'Microsoft Irina Desktop - Russian':
        engine.setProperty('voice', voices[i].id)   
    i+=1

#sleep(1)
engine.say(listen())
#engine.say(str(text))

engine.runAndWait()