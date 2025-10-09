import pyttsx3

tts_engine = pyttsx3.init()
tts_engine.setProperty("rate", 150)
tts_engine.setProperty("volume", 1.0)


def speak(text):
    for segment in text.split(". "):
        if segment.strip():
            tts_engine.say(segment.strip())
            tts_engine.runAndWait()
