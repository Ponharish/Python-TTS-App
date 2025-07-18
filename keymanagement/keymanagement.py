import boto3
import json
import sys
import os

import tkinter.messagebox
from tkinter import *

from keymanagement import pathresolver

from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError, EndpointConnectionError

def fileExists(filename):
    if os.path.exists(filename):
        return True
    else:
        return False

def retrieveKeys(filename):
    with open(filename, 'r') as file:
        keys = json.load(file)
    return keys

def retrieveFilePath(filename):
    return filename

def deleteKeyFile(filename):
    os.remove(filename)
