import langcodes
import pyttsx3

def getLanguages():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    languages = set()
    for voice in voices:
        if voice.languages:
            for lang in voice.languages:
                full_language_name = langcodes.get(lang).language_name()
                languages.add(str(lang) + " - " + full_language_name)
    langs = sorted(languages)        
    return langs
