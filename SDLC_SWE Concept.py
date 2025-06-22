import boto3
import pygame
import io

f = open('.secret_keys.txt', 'r')
keys = f.read()
keys = keys.split(',')
aws_access_key = keys[0].strip()
aws_secret_key = keys[1].strip()
region_name = 'ap-southeast-1'


text = """
<speak>
  Hi, <break time="300ms"/>
  Today, I will be explaining the software development life cycle.
  <break time="600ms"/>

  So, what exactly is the software development life cycle — or SDLC?
  <break time="600ms"/>

  Software development typically goes through stages like 
  requirements, analysis, design, implementation, and testing.
  <break time="500ms"/>

  These steps together form the software development life cycle.
  <break time="700ms"/>

  There are several approaches that describe different ways to go through the SDLC.
  Each process model gives developers a kind of roadmap for managing their work.
  <break time="500ms"/>

  This roadmap outlines the goals of each stage, the expected outcomes, and the workflow.
  <break time="700ms"/>

  Now, let’s start with the first approach:
  the Sequential model, also known as the Waterfall model.
  <break time="600ms"/>

  In this model, software development is seen as a linear process.
  When one stage is completed, it produces some artifacts to be used in the next stage.
  <break time="500ms"/>

  This model works excellent when solving a well-understood problem.
  <break time="500ms"/>

  But however, real-world projects often tackle problems that are not well-understood at the beginning,
  thus making them unsuitable for this model
  <break time="800ms"/>

  Let’s now move on to the Iterative model.
  <break time="500ms"/>

  In this approach, the software is built over multiple iterations.
  Each iteration may go through all the stages of the SDLC — from gathering requirements to deployment.
  <break time="600ms"/>

  There are two main ways to do this: 
  the breadth-first and, the depth-first approach.
  <break time="400ms"/>

  In the breadth-first approach, all major parts of the system evolve in parallel.
  <break time="300ms"/>
  It is ideal for projects that grow over time.
  <break time="600ms"/>

  In the depth-first approach, an iteration focuses on fleshing out only some components
  or some functionality area.
  So, early iterations might not produce a working product.
  <break time="600ms"/>

  It is also worth noting that projects can be done as a mixture of breadth-first and depth-first iterations.
  <break time="800ms"/>
  
  That wraps up this lesson. Thank you for listening.
  
  <break time="500ms"/>
  
  This content is adapted from the CS 2 1 0 3 website.
  <break time="600ms"/>
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
    Engine='neural'
)

audio_stream = response['AudioStream']

audio_bytes = audio_stream.read()

with open('sdlc.mp3', 'wb') as audio_file:
        audio_file.write(audio_bytes)

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(io.BytesIO(audio_bytes))
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(1)
