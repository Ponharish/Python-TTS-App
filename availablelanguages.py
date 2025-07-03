import boto3

def getAvailableLanguages(region, engine, awsAccessKey, awsSecretKey):
    polly = boto3.client(
        'polly',
        region_name=region,
        aws_access_key_id=awsAccessKey,
        aws_secret_access_key=awsSecretKey
    )

    voices = polly.describe_voices(Engine = engine.lower()) 
    languages = set()
    for voice in voices['Voices']:
        language_name = voice['LanguageName']
        languages.add(language_name)

    return sorted(languages)


