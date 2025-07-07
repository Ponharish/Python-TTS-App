import tts_aws

from keymanagement import keymanagement
from keymanagement import register

AWS_FILE_PATH = ".aws_keys.txt"
GOOGLE_FILE_PATH = ".google_key.json"

def main():
    #Check for keys
    if keymanagement.fileExists(AWS_FILE_PATH):
        tts_aws.startAppGui()
    elif keymanagement.fileExists(GOOGLE_FILE_PATH):
        print("Load Google Screen")
        pass #CHANGE LATER
        #load google gui
    else:
        register.registerKey()
        if keymanagement.fileExists(AWS_FILE_PATH):
            tts_aws.startAppGui()
        elif keymanagement.fileExists(GOOGLE_FILE_PATH):
            print("Load Google Screen")
            pass #CHANGE LATER
            #load google gui


main()
