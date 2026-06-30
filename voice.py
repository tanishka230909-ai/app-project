import pyttsx3

engine = pyttsx3.init()

engine.setProperty("rate", 150)

voices = engine.getProperty("voices")

if len(voices) > 1:
    engine.setProperty("voice", voices[1].id)


def speak(text):
    engine.say(text)
    engine.runAndWait()