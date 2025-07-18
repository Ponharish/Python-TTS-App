import boto3
import io
import pygame

from aws import availablelanguages
from aws import availableregions
from aws import availablevoices
from aws import characterusage

from keymanagement import changeservice
from keymanagement import keymanagement
from keymanagement import register

from audiomanager import playaudio

from botocore.exceptions import ClientError, EndpointConnectionError

from unidecode import unidecode

from tkinter import *

def startAppGui(AWS_FILE_PATH):
    global region
    
    def reconfigureKeys(): 
        root.destroy()
        changeservice.changeService()
        
    
    def reconfigureLanguage(*args):
        region = region_var.get()
        engine = engineVar.get()
        availableLanguages = availablelanguages.getAvailableLanguages(region, engineVar.get(), awsAccessKey, awsSecretKey)
        
        if 'US English' in availableLanguages:
            availableLanguages.remove('US English')
            availableLanguages.insert(0, 'US English')
        languageVar.set(availableLanguages[0])
        languageMenu['menu'].delete(0, 'end')
        for language in availableLanguages:
            languageMenu['menu'].add_command(label=language, command=lambda value=language: (languageVar.set(value), updateLanguage())) 

    def reconfigureVoice(*args):
        region = region_var.get()
        engine = engineVar.get()
        language = languageVar.get()

        availableVoices = availablevoices.getAvailableVoices(region, engine, language, awsAccessKey, awsSecretKey)
        voiceVar.set(availableVoices[0])
        voiceMenu['menu'].delete(0, 'end')
        for voice in availableVoices:
            voiceMenu['menu'].add_command(label=voice, command=lambda value=voice: (voiceVar.set(value), updateVoice()))
            
    def updateEngine():
        reconfigureLanguage()
        reconfigureVoice()
        
    def updateLanguage(*args):
        reconfigureVoice()
        
    def updateQuota():
        keys = keymanagement.retrieveKeys(AWS_FILE_PATH)
        awsAccessKey = keys['AWS_ACCESS_KEY_ID']
        awsSecretKey = keys['AWS_SECRET_ACCESS_KEY']
        statusLabel.config(text = characterusage.fetchUsage(awsAccessKey, awsSecretKey, region))

    def updateRegion(*args):
        global region
        region = region_var.get()
        updateQuota()
        reconfigureLanguage()
        reconfigureVoice()
        
    def updateVoice(*args):
        #nothing to be done at the moment
        pass
    
        
    def playAudio():
        global region
        errorLabel.config(text = "")
        
        keys = keymanagement.retrieveKeys(AWS_FILE_PATH)
        awsAccessKey = keys['AWS_ACCESS_KEY_ID']
        awsSecretKey = keys['AWS_SECRET_ACCESS_KEY']
        
        engine = engineVar.get()
        textType = textTypeVar.get()
        text = mainText.get("1.0", "end-1c")
        voice = voiceVar.get()
        voice = unidecode(voice)
        language = languageVar.get()

        if len(awsAccessKey)  ==  0 or len(awsSecretKey)  ==  0 or len(region)  ==  0:
            errorLabel.config(text = "Provide all inputs")
            return
        
        if len(text) > 2990:
           errorLabel.config(text = "The input provided is too long")
           return
        elif len(text)  ==  0:
           errorLabel.config(text = "Provide an Input text")
           return

        response = None
        try:
            polly_client = boto3.client(
                'polly',
                aws_access_key_id = awsAccessKey,
                aws_secret_access_key = awsSecretKey,
                region_name = region
            )
            response = polly_client.synthesize_speech(
                Text = text,
                OutputFormat = 'mp3',
                VoiceId = voice,
                Engine = engine,
                TextType = textType
            )
        except ClientError as e:
            error_code = e.response['Error']['Code']   
            if error_code  ==  'UnrecognizedClientException':
                errorLabel.config(text = "The AWS Access Key is invalid")
            elif error_code  ==  'InvalidSignatureException':
                errorLabel.config(text = "The AWS Secret Key is invalid")
            elif error_code  ==  'InvalidSsmlException':
                errorLabel.config(text = "The SSML input is invalid")
            else: 
                errorLabel.config(text = e)
            return
        except EndpointConnectionError as e:
            errorLabel.config(text = "The region is invalid")
            return
        except ValueError as e:
            errorLabel.config(text = "The region is invalid")
            return

        audio_stream = response['AudioStream']
        playaudio.playAudio(audio_stream.read())
        updateQuota()


    #GUI Interface
    root = Tk()
    root.title('Python TTS App')
    root.grid_rowconfigure(0, weight = 1)
    root.grid_columnconfigure(0, weight = 1)
    root.minsize(width=600, height=600)

    mainFrame = Frame(root, width = 700, height = 700, bg = "grey")
    mainFrame.grid(row = 0, column = 0, sticky = "nsew")
    mainFrame.grid_columnconfigure(0, weight = 1)

    #Header
    headerFrame = Frame(mainFrame, bg = "grey")
    headerFrame.grid(row = 0, column = 0, sticky = "nsew")
    headerFrame.grid_columnconfigure(0, weight = 1)

    headerLabel = Label(headerFrame, text = "Python TTS App", bg = "grey", anchor = "center", fg = "white", font = 'arial 39')
    headerLabel.grid(row = 0, column = 0, sticky = "nsew")

    #Credentials
    credentialsFrame = Frame(mainFrame, bg = "grey")
    credentialsFrame.grid(row = 1, column = 0, sticky = "nsew", pady = (10, 0))
    credentialsFrame.grid_rowconfigure(0, weight = 1)
    credentialsFrame.grid_rowconfigure(1, weight = 1)
    credentialsFrame.grid_rowconfigure(2, weight = 1)
    credentialsFrame.grid_columnconfigure(1, weight = 1)

    reconfigureKeysButton = Button(credentialsFrame, text = "Change Service", font = "Arial 20", bg = "blue", fg = "black", anchor = "center", command = reconfigureKeys)
    reconfigureKeysButton.grid(row = 0, column = 0, sticky = "nsew", padx = 30, pady = 10)
    reconfigureKeysButton.config(borderwidth = 2, relief = "solid", highlightthickness = 0, bd = 0)
    KeyLabel = Label(credentialsFrame, text = "AWS Keys are loaded from file", bg = "grey", anchor = "w", fg = "white", font = 'arial 20')
    KeyLabel.grid(row = 0, column =1, sticky = "nsew", padx = 30, pady = 10)
    KeyLabel.config(borderwidth = 2, relief = "solid", highlightthickness = 0, bd = 0)

    keys = keymanagement.retrieveKeys(AWS_FILE_PATH)
    awsAccessKey = keys['AWS_ACCESS_KEY_ID']
    awsSecretKey = keys['AWS_SECRET_ACCESS_KEY']
    regions = availableregions.getAvailableRegions(awsAccessKey, awsSecretKey)
    if 'ap-southeast-1' in regions:
        regions.remove('ap-southeast-1')
        regions.insert(0, 'ap-southeast-1')
    
    regionNameLabel = Label(credentialsFrame, text = "Region Name   ", bg = "grey", anchor = "e", fg = "white", font = 'arial 20')
    regionNameLabel.grid(row = 2, column = 0, sticky = "nsew", padx = 30, pady = 10)
    region_var = StringVar()
    region_var.set(regions[0])
    regionMenu = OptionMenu(credentialsFrame, region_var, *regions, command=updateRegion)
    # The below is code generated by ChatGPT that has been modified
    regionMenu.config(font=('Arial', 20), bg='grey', fg='black', relief='solid', bd=2, highlightthickness=0)
    regionMenu['menu'].config(font=('Arial', 15), bg='#ffffff', fg='black', relief='solid', bd=0)
    regionMenu.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)
    region = region_var.get()

    #TTS input
    inputFrame = Frame(mainFrame, bg = "grey")
    inputFrame.grid(row = 3, column = 0, sticky = "nsew", pady = (0, 0))
    inputFrame.grid_columnconfigure(1, weight = 1)

    #Engine Selection
    engineLabel = Label(inputFrame, text = "Engine", bg = "grey", anchor = "e", fg = "white", font = 'arial 20')
    engineLabel.grid(row = 0, column = 0, sticky = "nsew", padx = 30, pady = 5)
    engineVar = StringVar(value = "standard")
    engineFrame = Frame(inputFrame, bg = "grey")
    engineFrame.grid(row = 0, column = 1, sticky = "nsew", padx = 0, pady = 5)
    standardRadio = Radiobutton(engineFrame, text = "Standard", variable = engineVar, value = "standard", font = "Arial 20", bg = "grey", fg = "white", command=updateEngine)
    standardRadio.grid(row = 0, column = 0, sticky = "w", padx = 50, pady = 5)
    neuralRadio = Radiobutton(engineFrame, text = "Neural", variable = engineVar, value = "neural", font = "Arial 20", bg = "grey", fg = "white", command=updateEngine)
    neuralRadio.grid(row = 0, column = 1, sticky = "w", padx = 50, pady = 5)

    #Language Selection
    languageLabel = Label(inputFrame, text = "             Language", bg = "grey", anchor = "e", fg = "white", font = 'arial 20')
    languageLabel.grid(row = 1, column = 0, sticky = "nsew", padx = 30, pady = 5)
    languageVar = StringVar(value = "text")
    languages = availablelanguages.getAvailableLanguages(region, engineVar.get(), awsAccessKey, awsSecretKey)
    if 'US English' in languages:
        languages.remove('US English')
        languages.insert(0, 'US English')
    languageVar.set(languages[0])
    languageMenu = OptionMenu(inputFrame, languageVar, *languages, command=updateLanguage)
    # The below is code generated by ChatGPT that has been modified
    languageMenu.config(font=('Arial', 20), bg='grey', fg='black', relief='solid',  bd=2, highlightthickness=0)
    languageMenu['menu'].config(font=('Arial', 15), bg='#ffffff', fg='black', relief='solid', bd=0)
    languageMenu.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
    language = languageVar.get()

    #Voice Selection
    voiceLabel = Label(inputFrame, text = "                Voice", bg = "grey", anchor = "e", fg = "white", font = 'arial 20')
    voiceLabel.grid(row = 2, column = 0, sticky = "nsew", padx = 30, pady = 5)
    voiceVar = StringVar(value = "text")
    availableVoices = availablevoices.getAvailableVoices(region, engineVar.get(), language, awsAccessKey, awsSecretKey)
    voiceVar.set(availableVoices[0])
    voiceMenu = OptionMenu(inputFrame, voiceVar, *availableVoices, command=updateVoice)
    # The below is code generated by ChatGPT that has been modified
    voiceMenu.config(font=('Arial', 20), bg='grey', fg='black', relief='solid',  bd=2, highlightthickness=0)
    voiceMenu['menu'].config(font=('Arial', 15), bg='#ffffff', fg='black', relief='solid', bd=0)
    voiceMenu.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)
    voice = voiceVar.get()

    #Input Text Type
    textTypeLabel = Label(inputFrame, text = "            Text Type", bg = "grey", anchor = "e", fg = "white", font = 'arial 20')
    textTypeLabel.grid(row = 3, column = 0, sticky = "nsew", padx = 30, pady = 5)
    textTypeVar = StringVar(value = "text")
    textTypeFrame = Frame(inputFrame, bg = "grey")
    textTypeFrame.grid(row = 3, column = 1, sticky = "nsew", padx = 0, pady = 5)
    textRadio = Radiobutton(textTypeFrame, text = "Text        ", variable = textTypeVar, value = "text", font = "Arial 20", bg = "grey", fg = "white")
    textRadio.grid(row = 0, column = 0, sticky = "w", padx = 50, pady = 5)
    ssmlRadio = Radiobutton(textTypeFrame, text = "SSML    ", variable = textTypeVar, value = "ssml", font = "Arial 20", bg = "grey", fg = "white")
    ssmlRadio.grid(row = 0, column = 1, sticky = "w", padx = 50, pady = 5)

    #Text to be converted to speech
    mainTextLabel = Label(inputFrame, text = "Text", bg = "grey", anchor = "e", fg = "white", font = 'arial 20')
    mainTextLabel.grid(row = 4, column = 0, sticky = "nsew", padx = 30, pady = 5)
    mainText = Text(inputFrame, height = 10, width = 50, font = 'Arial 20', wrap = "word", bg = "white", fg = "black")
    mainText.grid(row = 4, column = 1, sticky = "nsew", padx = 30, pady = 5)
    mainText.config(borderwidth = 2, relief = "solid", highlightthickness = 0, bd = 0)

    #Submit button
    submitFrame = Frame(mainFrame, bg = "grey")
    submitFrame.grid(row = 4, column = 0, sticky = "nsew", pady = (10, 0))
    submitFrame.grid_columnconfigure(0, weight = 1)
    submitButton = Button(submitFrame, text = "Submit", font = "Arial 20", bg = "blue", fg = "black", anchor = "center", command = playAudio)
    submitButton.pack(side = "bottom", pady = 5)
    submitButton.config(borderwidth = 2, relief = "solid", highlightthickness = 0, bd = 0)

    #Errors
    errorFrame = Frame(mainFrame, bg = "grey")
    errorFrame.grid(row = 5, column = 0, sticky = "nsew", pady = (10, 0))
    errorFrame.grid_columnconfigure(0, weight = 1)
    errorLabel = Label(errorFrame, text = "", anchor = "center", bg = "grey", fg = "#9D0000", font = "Arial 18")
    errorLabel.grid(row = 0, column = 0, sticky = "nsew", padx = 30, pady = 10)


    #Status - remaining characters
    statusLabel = Label(root, text = "Usage: ", anchor = "sw", bg = "yellow", fg = "#000000", font = "Arial 15")
    statusLabel.grid(row = 6, column = 0, sticky = "nsew")
    statusInfoLabel = Label(root, text = "[Usage Updates every 2 mins]", anchor = "sw", bg = "yellow", fg = "grey", font = "Arial 15")
    statusInfoLabel.grid(row = 7, column = 0, sticky = "nsew")
    updateQuota()

    root.mainloop()
