from google.oauth2 import service_account
from google.cloud import texttospeech
from google.api_core.exceptions import GoogleAPIError

def getEngines(keyPath, language):
    credentials = service_account.Credentials.from_service_account_file(keyPath)
    client = texttospeech.TextToSpeechClient(credentials=credentials)
    response = client.list_voices()
    engines = set()
    for voice in response.voices:
        voiceName = voice.name
        if language in voiceName:
            voiceName = voiceName.split('-')
            voiceName.pop(0)
            voiceName.pop(0)
            voiceName.pop(-1)
            voiceName = '-'.join(voiceName)
            engines.add(voiceName)
    engines = sorted(engines)
    return engines
