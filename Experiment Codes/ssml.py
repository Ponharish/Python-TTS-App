import boto3
import pygame
import io

f = open('../.secret_keys.txt', 'r')
keys = f.read()
keys = keys.split(',')
aws_access_key = keys[0].strip()
aws_secret_key = keys[1].strip()
region_name = 'ap-southeast-1'

text = """
    <speak>
        Hello, <break time="500ms"/> 
        <emphasis level="strong">world</emphasis>!
        Here is a number: <say-as interpret-as="cardinal">12345</say-as>.
        And a date: <say-as interpret-as="date" format="ymd">2025-06-19</say-as>.
    </speak>
    """

polly_client = boto3.client(
    'polly',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=region_name
)
    
response = polly_client.synthesize_speech(
    Text=text,
    OutputFormat='mp3',
    VoiceId='Joanna',
    TextType='ssml',      
    Engine='standard' 
)

audio_stream = response['AudioStream']

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(io.BytesIO(audio_stream.read()))
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(1)
