import boto3
import json
import os
import shutil
import sys

import tkinter.messagebox
from tkinter import *
from tkinter import filedialog

from google.oauth2 import service_account
from google.cloud import texttospeech
from google.api_core.exceptions import GoogleAPIError

from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError, EndpointConnectionError

def registerKey():
    def selectService():
        service = serviceVar.get()
        root.destroy()
        if service == "AWS":
            loadAwsKey()
        elif service == "Google":
            loadGoogleKey()
        else:
            loadOsKey()

        
    root = Tk()
    root.title('Python TTS App')
    root.grid_rowconfigure(0, weight = 1)
    root.grid_columnconfigure(0, weight = 1)
    root.minsize(width = 800, height = 200)

    mainFrame = Frame(root, width = 700, height = 400, bg = "grey")
    mainFrame.grid(row = 0, column = 0, sticky = "nsew")
    mainFrame.grid_columnconfigure(0, weight = 1)

    #Header
    headerFrame = Frame(mainFrame, bg = "grey")
    headerFrame.grid(row = 0, column = 0, sticky = "nsew")
    headerFrame.grid_columnconfigure(0, weight = 1)

    headerLabel = Label(headerFrame, text = "Key Management", bg = "grey", anchor = "center", fg = "white", font = 'arial 29')
    headerLabel.grid(row = 0, column = 0, sticky = "nsew")
    infoLabel = Label(headerFrame,
                      text = "\nChoose your TTS Service",
                      bg = "grey", anchor = "w", fg = "white",font = 'arial 20', padx = 30)
    infoLabel.grid(row = 2, column = 0, sticky = "nsew")


    serviceVar = StringVar(value = "AWS")
    serviceFrame = Frame(mainFrame, bg = "grey")
    serviceFrame.grid(row = 1, column = 0, sticky = "nsew", pady = (10, 0))
    awsRadio = Radiobutton(serviceFrame, text = "AWS", variable = serviceVar, value = "AWS", font = "Arial 20", bg = "grey", fg = "white")
    awsRadio.grid(row = 0, column = 0, sticky = "w", padx = 50, pady = 5)
    googleRadio = Radiobutton(serviceFrame, text = "Google Cloud", variable = serviceVar, value = "Google", font = "Arial 20", bg = "grey", fg = "white")
    googleRadio.grid(row = 0, column = 1, sticky = "w", padx = 50, pady = 5)
    osRadio = Radiobutton(serviceFrame, text = "OS Native TTS", variable = serviceVar, value = "OS", font = "Arial 20", bg = "grey", fg = "white")
    osRadio.grid(row = 0, column = 2, sticky = "w", padx = 50, pady = 5)

    
    #Submit button
    submitFrame = Frame(mainFrame, bg = "grey")
    submitFrame.grid(row = 2, column = 0, sticky = "nsew", pady = (10, 0))
    submitFrame.grid_columnconfigure(0, weight = 1)
    submitButton = Button(submitFrame, text = "Next", font = "Arial 20", bg = "blue", fg = "black", anchor = "center", command = selectService)
    submitButton.pack(side = "bottom", pady = 5)
    submitButton.config(borderwidth = 2, relief = "solid", highlightthickness = 0, bd = 0)

    root.mainloop()

    
    
def loadAwsKey():
    def validateKeys(awsAccessKey, awsSecretKey):
        session = boto3.Session(
            aws_access_key_id = awsAccessKey,
            aws_secret_access_key = awsSecretKey,
            region_name = 'ap-southeast-1'
        )

        polly_client = session.client('polly')

        try:
            # A simple ops to validate the given keys
            response = polly_client.describe_voices()
            return True  # Valid credentials
        except NoCredentialsError:
            errorLabel.config(text = "No credentials found. Please provide valid AWS keys")
        except PartialCredentialsError:
            errorLabel.config(text = "Incomplete credentials. Please check the AWS keys")
        except EndpointConnectionError:
            errorLabel.config(text = "Could not connect to AWS Polly. Check your network connection")
        except ClientError as e:
            error_code = e.response['Error']['Code']   
            if error_code == 'UnrecognizedClientException':
                errorLabel.config(text = "The AWS Access Key is invalid")
            elif error_code == 'InvalidSignatureException':
                errorLabel.config(text = "The AWS Secret Key is invalid")
        except Exception as e:
            errorLabel.config(text = "An Error has occured. Please try again later")
        return False

    def saveKeys(access_key, secret_key, filename = ".aws_keys.txt"):
        keys = {"AWS_ACCESS_KEY_ID": access_key, "AWS_SECRET_ACCESS_KEY": secret_key}
        with open(filename, 'w') as file:
            json.dump(keys, file)

    def processKeys():
        awsAccessKey = accessKey.get()
        awsSecretKey = secretKey.get()
        
        if not validateKeys(awsAccessKey, awsSecretKey):
            return
        saveKeys(awsAccessKey, awsSecretKey)
        tkinter.messagebox.showinfo("Key Management", "The keys have been saved")
        root.destroy()

    root = Tk()
    root.title('Python TTS App')
    root.grid_rowconfigure(0, weight = 1)
    root.grid_columnconfigure(0, weight = 1)
    root.minsize(width = 800, height = 200)

    mainFrame = Frame(root, width = 700, height = 400, bg = "grey")
    mainFrame.grid(row = 0, column = 0, sticky = "nsew")
    mainFrame.grid_columnconfigure(0, weight = 1)

    #Header
    headerFrame = Frame(mainFrame, bg = "grey")
    headerFrame.grid(row = 0, column = 0, sticky = "nsew")
    headerFrame.grid_columnconfigure(0, weight = 1)

    headerLabel = Label(headerFrame, text = "Key Management", bg = "grey", anchor = "center", fg = "white", font = 'arial 29')
    headerLabel.grid(row = 0, column = 0, sticky = "nsew")

    infoLabel = Label(headerFrame,
                      text = "\nEnter your AWS credentials below to be saved.      ",
                      bg = "grey", anchor = "w", fg = "white",font = 'arial 20', padx = 30)
    infoLabel.grid(row = 2, column = 0, sticky = "nsew")

    #Credentials
    credentialsFrame = Frame(mainFrame, bg = "grey")
    credentialsFrame.grid(row = 1, column = 0, sticky = "nsew", pady = (10, 0))
    credentialsFrame.grid_rowconfigure(0, weight = 1)
    credentialsFrame.grid_rowconfigure(1, weight = 1)
    credentialsFrame.grid_rowconfigure(2, weight = 1)
    credentialsFrame.grid_columnconfigure(1, weight = 1)

    accessKeyLabel = Label(credentialsFrame, text = "AWS Access Key", bg = "grey", anchor = "e", fg = "white", font = 'arial 20')
    accessKeyLabel.grid(row = 0, column = 0, sticky = "nsew", padx = 30, pady = 10)
    accessKey = Entry(credentialsFrame, bd = 0, highlightthickness = 0, relief = "flat", font = "Arial 20", bg = "white", fg = "black")
    accessKey.grid(row = 0, column = 1, sticky = "nsew", padx = 50, pady = 10)
    accessKey.config(borderwidth = 2, relief = "solid", highlightthickness = 0, bd = 0)

    secretKeyLabel = Label(credentialsFrame, text = "AWS Secret Key", bg = "grey", anchor = "e", fg = "white", font = 'arial 20')
    secretKeyLabel.grid(row = 1, column = 0, sticky = "nsew", padx = 30, pady = 10)
    secretKey = Entry(credentialsFrame, bd = 0, highlightthickness = 0, relief = "flat", font = "Arial 20", bg = "white", fg = "black")
    secretKey.grid(row = 1, column = 1, sticky = "nsew", padx = 50, pady = 10)
    secretKey.config(borderwidth = 2, relief = "solid", highlightthickness = 0, bd = 0)

    #Submit button
    submitFrame = Frame(mainFrame, bg = "grey")
    submitFrame.grid(row = 2, column = 0, sticky = "nsew", pady = (10, 0))
    submitFrame.grid_columnconfigure(0, weight = 1)
    submitButton = Button(submitFrame, text = "Save", font = "Arial 20", bg = "blue", fg = "black", anchor = "center", command = processKeys)
    submitButton.pack(side = "bottom", pady = 5)
    submitButton.config(borderwidth = 2, relief = "solid", highlightthickness = 0, bd = 0)

    #Errors
    errorFrame = Frame(mainFrame, bg = "grey")
    errorFrame.grid(row = 5, column = 0, sticky = "nsew", pady = (10, 0))
    errorFrame.grid_columnconfigure(0, weight = 1)
    errorLabel = Label(errorFrame, text = "", anchor = "center", bg = "grey", fg = "#9D0000", font = "Arial 18")
    errorLabel.grid(row = 0, column = 0, sticky = "nsew", padx = 30, pady = 10)

    root.mainloop()

def loadGoogleKey():
    def validateKey(keyPath):
        # A simple ops to validate the key
        try:
            credentials = service_account.Credentials.from_service_account_file(keyPath)
            client = texttospeech.TextToSpeechClient(credentials=credentials)          
            response = client.list_voices()
            return True
        except GoogleAPIError as e:
            errorLabel.config(text = "Google API Error")
            return False
        except Exception as e:
            
            errorLabel.config(text = "Invalid key or other error")
            return False


    def openFile():
        appKeyPath = os.path.expanduser("./.google_key.json")
        keyPath = filedialog.askopenfilename(
            title="Select Google TTS Service Account JSON Key",
            filetypes=[("JSON Files", "*.json")]
        )

        if not keyPath:
            return

        if not validateKey(keyPath):
            return

        try:
            os.makedirs(os.path.dirname(appKeyPath), exist_ok=True)
            shutil.copy(keyPath, appKeyPath)
            tkinter.messagebox.showinfo("Key Management", "The key has been saved")
            root.destroy()
        except Exception as e:
            print(e)
            errorLabel.config(text = "Error: Failed to load Key")           

    root = Tk()
    root.title('Python TTS App')
    root.grid_rowconfigure(0, weight = 1)
    root.grid_columnconfigure(0, weight = 1)
    root.minsize(width = 800, height = 200)

    mainFrame = Frame(root, width = 700, height = 400, bg = "grey")
    mainFrame.grid(row = 0, column = 0, sticky = "nsew")
    mainFrame.grid_columnconfigure(0, weight = 1)

    #Header
    headerFrame = Frame(mainFrame, bg = "grey")
    headerFrame.grid(row = 0, column = 0, sticky = "nsew")
    headerFrame.grid_columnconfigure(0, weight = 1)

    headerLabel = Label(headerFrame, text = "Key Management", bg = "grey", anchor = "center", fg = "white", font = 'arial 29')
    headerLabel.grid(row = 0, column = 0, sticky = "nsew")

    infoLabel = Label(headerFrame,
                      text = "\nSelect the JSON file containing your google service account key",
                      bg = "grey", anchor = "w", fg = "white",font = 'arial 20', padx = 30)
    infoLabel.grid(row = 2, column = 0, sticky = "nsew")

    #File Browse button
    openFileFrame = Frame(mainFrame, bg = "grey")
    openFileFrame.grid(row = 1, column = 0, sticky = "nsew", pady = (10, 0))
    openFileFrame.grid_columnconfigure(0, weight = 1)
    openFileButton = Button(openFileFrame, text = "Open File", font = "Arial 20", bg = "blue", fg = "black", anchor = "center", command = openFile)
    openFileButton.pack(side = "bottom", pady = 5)
    openFileButton.config(borderwidth = 2, relief = "solid", highlightthickness = 0, bd = 0)

    #Errors
    errorFrame = Frame(mainFrame, bg = "grey")
    errorFrame.grid(row = 2, column = 0, sticky = "nsew", pady = (10, 0))
    errorFrame.grid_columnconfigure(0, weight = 1)
    errorLabel = Label(errorFrame, text = "", anchor = "center", bg = "grey", fg = "#9D0000", font = "Arial 18")
    errorLabel.grid(row = 0, column = 0, sticky = "nsew", padx = 30, pady = 10)

    root.mainloop()

def loadOsKey():
    with open('.os_tts.txt', 'w') as file:
        file.write("Os tts Cache")
