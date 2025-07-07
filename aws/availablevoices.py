import boto3

# The below function is to handle those edge cases when language name includes a ( and ).
# Eg: English (US) instead of US English
def normalizeLanguage(language):
    if '(' in language and ')' in language:
        parts = language.split('(')
        language = parts[1].split(')')[0] + ' ' + parts[0].strip()
    return language

def getAvailableVoices(region, engine, language, awsAccessKey, awsSecretKey):
    language = normalizeLanguage(language)
    polly = boto3.client(
        'polly',
        region_name=region, 
        aws_access_key_id=awsAccessKey,
        aws_secret_access_key=awsSecretKey
    )

    voices = polly.describe_voices(Engine=engine.lower())

    people = set()
    for voice in voices['Voices']:
        if voice['LanguageName'] == language:
            people.add(voice['Name'])
    return sorted(people)
