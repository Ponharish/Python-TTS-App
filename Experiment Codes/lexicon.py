import boto3
import pygame
import io

#The following code has been partially generated using ChatGpt

f = open('../.secret_keys.txt', 'r')
keys = f.read()
keys = keys.split(',')
aws_access_key = keys[0].strip()
aws_secret_key = keys[1].strip()
region_name = 'ap-southeast-1'

polly = boto3.client(
    'polly',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=region_name
)
lexicon_name = 'MyCustomLexicon'
lexicon_content = """
<lexicon version="1.0" 
         xmlns="http://www.w3.org/2005/01/pronunciation-lexicon"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
         xsi:schemaLocation="http://www.w3.org/2005/01/pronunciation-lexicon 
                             http://www.w3.org/2005/01/pronunciation-lexicon/lexicon.xsd" 
         alphabet="ipa" 
         xml:lang="en-US">
  <lexeme>
    <grapheme>pecan</grapheme>
    <phoneme>/ˈæp.əl/</phoneme>
  </lexeme>
</lexicon>
"""

polly.put_lexicon(Name=lexicon_name, Content=lexicon_content)
text = "How do you pronounce pecan pie?"

response = polly.synthesize_speech(
    Text=text,
    OutputFormat='mp3',
    VoiceId='Joanna',
    LexiconNames=[lexicon_name]
)


audio_stream = response['AudioStream']

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(io.BytesIO(audio_stream.read()))
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(1)
