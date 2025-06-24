import boto3
import io
import pygame

from botocore.exceptions import ClientError, EndpointConnectionError

from tkinter import *

def playAudio():
    awsAccessKey = accessKey.get()
    awsSecretKey = secretKey.get()
    region = regionName.get()
    engine = engineVar.get()
    textType = textTypeVar.get()
    text = mainText.get("1.0", "end-1c")

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
            VoiceId = 'Joanna',
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

    errorLabel.config(text = "")
    audio_stream = response['AudioStream']

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(io.BytesIO(audio_stream.read()))
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(1)


root = Tk()
root.title('Python TTS App')
root.grid_rowconfigure(0, weight = 1)
root.grid_columnconfigure(0, weight = 1)
root.minsize(width=600, height=400)

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

regionNameLabel = Label(credentialsFrame, text = "Region Name", bg = "grey", anchor = "e", fg = "white", font = 'arial 20')
regionNameLabel.grid(row = 2, column = 0, sticky = "nsew", padx = 30, pady = 10)
regionName = Entry(credentialsFrame, bd = 0, highlightthickness = 0, relief = "flat", font = "Arial 20", bg = "white", fg = "black")
regionName.grid(row = 2, column = 1, sticky = "nsew", padx = 50, pady = 10)
regionName.config(borderwidth = 2, relief = "solid", highlightthickness = 0, bd = 0)

#HR
canvas = Canvas(mainFrame, height = 2, width = 500, bg = "grey", bd = 0, highlightthickness = 0)
canvas.create_line(0, 1, 50000, 1, fill = "white", width = 2)
canvas.grid(row = 2, column = 0, sticky = "nsew", pady = 10)


#TTS input
inputFrame = Frame(mainFrame, bg = "grey")
inputFrame.grid(row = 3, column = 0, sticky = "nsew", pady = (0, 0))
inputFrame.grid_columnconfigure(1, weight = 1)

engineLabel = Label(inputFrame, text = "Engine", bg = "grey", anchor = "e", fg = "white", font = 'arial 20')
engineLabel.grid(row = 0, column = 0, sticky = "nsew", padx = 30, pady = 5)
engineVar = StringVar(value = "standard")
engineFrame = Frame(inputFrame, bg = "grey")
engineFrame.grid(row = 0, column = 1, sticky = "nsew", padx = 0, pady = 5)
standardRadio = Radiobutton(engineFrame, text = "Standard", variable = engineVar, value = "standard", font = "Arial 20", bg = "grey", fg = "white")
standardRadio.grid(row = 0, column = 0, sticky = "w", padx = 50, pady = 5)
neuralRadio = Radiobutton(engineFrame, text = "Neural", variable = engineVar, value = "neural", font = "Arial 20", bg = "grey", fg = "white")
neuralRadio.grid(row = 0, column = 1, sticky = "w", padx = 50, pady = 5)

textTypeLabel = Label(inputFrame, text = "            Text Type", bg = "grey", anchor = "e", fg = "white", font = 'arial 20')
textTypeLabel.grid(row = 1, column = 0, sticky = "nsew", padx = 30, pady = 5)
textTypeVar = StringVar(value = "text")
textTypeFrame = Frame(inputFrame, bg = "grey")
textTypeFrame.grid(row = 1, column = 1, sticky = "nsew", padx = 0, pady = 5)
textRadio = Radiobutton(textTypeFrame, text = "Text        ", variable = textTypeVar, value = "text", font = "Arial 20", bg = "grey", fg = "white")
textRadio.grid(row = 0, column = 0, sticky = "w", padx = 50, pady = 5)
ssmlRadio = Radiobutton(textTypeFrame, text = "SSML    ", variable = textTypeVar, value = "ssml", font = "Arial 20", bg = "grey", fg = "white")
ssmlRadio.grid(row = 0, column = 1, sticky = "w", padx = 50, pady = 5)

mainTextLabel = Label(inputFrame, text = "Text", bg = "grey", anchor = "e", fg = "white", font = 'arial 20')
mainTextLabel.grid(row = 3, column = 0, sticky = "nsew", padx = 30, pady = 5)
mainText = Text(inputFrame, height = 10, width = 50, font = 'Arial 20', wrap = "word", bg = "white", fg = "black")
mainText.grid(row = 3, column = 1, sticky = "nsew", padx = 30, pady = 5)
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

root.mainloop()
