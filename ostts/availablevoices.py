import pyttsx3

def getVoices(language):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    voiceSet = set()
    for voice in voices:
        if hasattr(voice, 'languages') and voice.languages:
            for lang in voice.languages:
                if str(lang) == language:
                    voiceSet.add(str(voice.name))

    voiceList = sorted(voiceSet)        
    return voiceList
