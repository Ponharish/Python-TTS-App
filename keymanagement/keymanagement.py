import boto3
import json
import sys
import os

import tkinter.messagebox
from tkinter import *

from keymanagement import pathresolver

from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError, EndpointConnectionError

def fileExists(filename):
    if os.path.exists(pathresolver.get_key_file_path(filename)):
        return True
    else:
        return False

def retrieveKeys(filename):
    with open(pathresolver.get_key_file_path(filename), 'r') as file:
        keys = json.load(file)
    return keys

def retrieveFilePath(filename):
    return pathresolver.get_key_file_path(filename)

def deleteKeyFile(filename):
    os.remove(pathresolver.get_key_file_path(filename))
