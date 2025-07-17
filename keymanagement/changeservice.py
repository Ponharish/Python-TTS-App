from keymanagement import keymanagement
from keymanagement import register

import tts_aws
import tts_google

AWS_FILE_PATH = ".aws_keys.txt"
GOOGLE_FILE_PATH = ".google_key.json"

def changeService():
    if keymanagement.fileExists(AWS_FILE_PATH):
        keymanagement.deleteKeyFile(AWS_FILE_PATH)
    elif keymanagement.fileExists(GOOGLE_FILE_PATH):
        keymanagement.deleteKeyFile(GOOGLE_FILE_PATH)
        
    register.registerKey()
    
    if keymanagement.fileExists(AWS_FILE_PATH):
        tts_aws.startAppGui()
    elif keymanagement.fileExists(GOOGLE_FILE_PATH):
        tts_google.startAppGui()

    
        
