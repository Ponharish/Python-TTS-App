from keymanagement import keymanagement
from keymanagement import register

import tts_aws

AWS_FILE_PATH = ".aws_keys.txt"
GOOGLE_FILE_PATH = ""#CHANGE THIS LATER

def changeService():
    if keymanagement.fileExists(AWS_FILE_PATH):
        keymanagement.deleteKeyFile(AWS_FILE_PATH)
    elif keymanagement.fileExists(GOOGLE_FILE_PATH):
        keymanagement.deleteKeyFile(GOOGLE_FILE_PATH)
        
    register.registerKey()
    
    if keymanagement.fileExists(AWS_FILE_PATH):
        tts_aws.startAppGui()
    elif keymanagement.fileExists(GOOGLE_FILE_PATH):
        pass #CHANGE LATER
        #load google gui
        
    
        
