import tts_aws

from keymanagement import keymanagement
from keymanagement import register

AWS_FILE_PATH = ".aws_keys.txt"
GOOGLE_FILE_PATH = ""#CHANGE THIS LATER

def main():
    #Check for keys
    if keymanagement.fileExists(AWS_FILE_PATH):
        tts_aws.startAppGui()
    elif keymanagement.fileExists(GOOGLE_FILE_PATH):
        pass #CHANGE LATER
        #load google gui
    else:
        register.registerKey()
        if keymanagement.fileExists(AWS_FILE_PATH):
            tts_aws.startAppGui()
        elif keymanagement.fileExists(GOOGLE_FILE_PATH):
            pass #CHANGE LATER
            #load google gui


main()
