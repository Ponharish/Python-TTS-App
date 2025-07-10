from google.oauth2 import service_account
from google.cloud import texttospeech
from google.api_core.exceptions import GoogleAPIError

def getVoices(keyPath, language, engine, gender):
    credentials = service_account.Credentials.from_service_account_file(keyPath)
    client = texttospeech.TextToSpeechClient(credentials=credentials)
    response = client.list_voices()
    voices = set()
    for voice in response.voices:
        voiceName = voice.name      
        currGender = texttospeech.SsmlVoiceGender(voice.ssml_gender).name
        if (language + '-' + engine) in voiceName and currGender == gender:
            voices.add(voiceName)
    voices = sorted(voices)
    return voices
