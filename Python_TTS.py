import tts_aws
import tts_google
import tts_os

from keymanagement import keymanagement
from keymanagement import register

AWS_FILE_PATH = ".aws_keys.txt"
GOOGLE_FILE_PATH = ".google_key.json"
OSTTS_FILE_PATH = ".os_tts.txt"

def main():
    #Check for keys
    if keymanagement.fileExists(AWS_FILE_PATH):
        tts_aws.startAppGui()
    elif keymanagement.fileExists(GOOGLE_FILE_PATH):
        tts_google.startAppGui()
    elif keymanagement.fileExists(OSTTS_FILE_PATH):
        tts_os.startAppGui()
    else:
        register.registerKey()
        if keymanagement.fileExists(AWS_FILE_PATH):
            tts_aws.startAppGui()
        elif keymanagement.fileExists(GOOGLE_FILE_PATH):
            tts_google.startAppGui()
        elif keymanagement.fileExists(OSTTS_FILE_PATH):
            tts_os.startAppGui()

main()
