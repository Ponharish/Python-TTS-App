from google.oauth2 import service_account
from google.cloud import texttospeech
from google.api_core.exceptions import GoogleAPIError
import langcodes

def getLanguages(keyPath):
    credentials = service_account.Credentials.from_service_account_file(keyPath)
    client = texttospeech.TextToSpeechClient(credentials=credentials)
    response = client.list_voices()
    languages = set()
    for voice in response.voices:
        for language in voice.language_codes:
            full_language_name = langcodes.get(language).language_name()
            languages.add(language + " - " + full_language_name)
    langs = sorted(languages)        
    return langs
