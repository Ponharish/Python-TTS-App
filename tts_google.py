import io
import pygame

from tkinter import *

from googletts import availablelanguages
from googletts import availablevoices
from googletts import availableengines

from keymanagement import changeservice
from keymanagement import keymanagement
from keymanagement import register

from google.oauth2 import service_account
from google.cloud import texttospeech
from google.api_core.exceptions import GoogleAPIError

from keymanagement import pathresolver

from audiomanager import playaudio

def startAppGui(GOOGLE_FILE_PATH):
    def get_all_toplevels(root):
        return [w for w in root.winfo_children() if isinstance(w, Toplevel)]

    def reconfigureKeys():
        for win in get_all_toplevels(root):
            win.destroy()
        playaudio.stopMusic()
        root.destroy()
        changeservice.changeService()
    
    def reconfigureEngine(*args):
        language = languageVar.get()
        language = language.split(' - ')[0]   
        engines = availableengines.getEngines(GOOGLE_FILE_PATH, language)
        if 'Standard' in engines:
            engines.remove('Standard')
            engines.insert(0, 'Standard')
        engineVar.set(engines[0])   
        engineMenu['menu'].delete(0, 'end')
        for engine in engines:
            engineMenu['menu'].add_command(label=engine, command=lambda value=engine: (engineVar.set(value), updateEngine()))

    def reconfigureVoice(*args):
        gender = genderVar.get()
        engine = engineVar.get()
        language = languageVar.get()
        language = language.split(' - ')[0] 
        availableVoices = availablevoices.getVoices(GOOGLE_FILE_PATH, language, engine, gender)
        if availableVoices:
            voiceVar.set(availableVoices[0])
        else:
            voiceVar.set("No Voices Available")
        voiceMenu['menu'].delete(0, 'end')
        for voice in availableVoices:
            voiceMenu['menu'].add_command(label=voice, command=lambda value=voice: (voiceVar.set(value), updateVoice()))
            
    def updateEngine(*args):
        reconfigureVoice()

    def updateGender():
        reconfigureVoice()
        
    def updateLanguage(*args):
        reconfigureEngine()
        reconfigureVoice()
        
    def updateQuota():
        # To be completed in a future iteration
        pass
        
    def updateVoice(*args):
        #nothing to be done at the moment
        pass
    
        
    def playAudio():
        errorLabel.config(text = "")
        engine = engineVar.get()
        textType = textTypeVar.get()
        text = mainText.get("1.0", "end-1c")
        voice = voiceVar.get()
        gender = genderVar.get()
        language = languageVar.get()
        language = language.split(' - ')[0]   

        if voice == "No Voices Available":
            errorLabel.config(text = "Please select a valid voice")
            return

        if len(text) > 4990:
           errorLabel.config(text = "The input provided is too long")
           return
        elif len(text)  ==  0:
           errorLabel.config(text = "Provide an Input text")
           return

        response = None
        ssmlGender = texttospeech.SsmlVoiceGender.MALE
        if gender == "FEMALE":
            ssmlGender = texttospeech.SsmlVoiceGender.FEMALE
        elif gender == "NEUTRAL":
            ssmlGender = texttospeech.SsmlVoiceGender.NEUTRAL
        try:
            credentials = service_account.Credentials.from_service_account_file(GOOGLE_FILE_PATH)
            client = texttospeech.TextToSpeechClient(credentials = credentials)
            synthesis_input = None
            if textType == 'text':
                synthesis_input = texttospeech.SynthesisInput(text = text)
            elif textType == 'ssml':
                synthesis_input = texttospeech.SynthesisInput(ssml = text)

            voice = texttospeech.VoiceSelectionParams(
                language_code = language,
                name = voice,
                ssml_gender = ssmlGender
            )

            audio_config = texttospeech.AudioConfig(
                audio_encoding = texttospeech.AudioEncoding.MP3
            )

            response = client.synthesize_speech(
                input = synthesis_input,
                voice = voice,
                audio_config = audio_config
            )
        except Exception as e:
            errorLabel.config(text = "An error has occured")
            return

        if response == None:
            errorLabel.config(text = "An error has occured")
            return

        playaudio.playAudio(response.audio_content, root)

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
    credentialsFrame.grid_columnconfigure(1, weight = 1)

    reconfigureKeysButton = Button(credentialsFrame, text = "Change Service", font = "Arial 20", fg = "black", anchor = "center", command = reconfigureKeys)
    reconfigureKeysButton.grid(row = 0, column = 0, sticky = "nsew", padx = 30, pady = 10)
    reconfigureKeysButton.config(borderwidth = 2, relief = "solid", highlightthickness = 0, bd = 0)
    KeyLabel = Label(credentialsFrame, text = "Google Cloud Key is loaded from file", bg = "grey", anchor = "w", fg = "white", font = 'arial 20')
    KeyLabel.grid(row = 0, column =1, sticky = "nsew", padx = 30, pady = 10)
    KeyLabel.config(borderwidth = 2, relief = "solid", highlightthickness = 0, bd = 0)


    #TTS input
    inputFrame = Frame(mainFrame, bg = "grey")
    inputFrame.grid(row = 3, column = 0, sticky = "nsew", pady = (0, 0))
    inputFrame.grid_columnconfigure(1, weight = 1)

    #Language Selection
    languageLabel = Label(inputFrame, text = "             Language", bg = "grey", anchor = "e", fg = "white", font = 'arial 20')
    languageLabel.grid(row = 0, column = 0, sticky = "nsew", padx = 30, pady = 5)
    languageVar = StringVar(value = "text")
    languages = availablelanguages.getLanguages(GOOGLE_FILE_PATH)   
    if 'en-US - English' in languages:
        languages.remove('en-US - English')
        languages.insert(0, 'en-US - English')
    languageVar.set(languages[0])
    languageMenu = OptionMenu(inputFrame, languageVar, *languages, command=updateLanguage)
    languageMenu.config(font=('Arial', 20), bg='grey', fg='black', relief='solid',  bd=2, highlightthickness=0)
    languageMenu['menu'].config(font=('Arial', 15), bg='#ffffff', fg='black', relief='solid', bd=0)
    languageMenu.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    language = languageVar.get()
    language = language.split(' - ')[0]

    #Engine Selection
    engineLabel = Label(inputFrame, text = "Engine", bg = "grey", anchor = "e", fg = "white", font = 'arial 20')
    engineLabel.grid(row = 1, column = 0, sticky = "nsew", padx = 30, pady = 5)
    engineVar = StringVar(value = "text")
    engines = availableengines.getEngines(GOOGLE_FILE_PATH, language)   
    if 'Standard' in engines:
        engines.remove('Standard')
        engines.insert(0, 'Standard')
    engineVar.set(engines[0])
    engineMenu = OptionMenu(inputFrame, engineVar, *engines, command=updateEngine)
    engineMenu.config(font=('Arial', 20), bg='grey', fg='black', relief='solid',  bd=2, highlightthickness=0)
    engineMenu['menu'].config(font=('Arial', 15), bg='#ffffff', fg='black', relief='solid', bd=0)
    engineMenu.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
    engine = engineVar.get()

    #Gender Selection
    genderLabel = Label(inputFrame, text = "Gender", bg = "grey", anchor = "e", fg = "white", font = 'arial 20')
    genderLabel.grid(row = 2, column = 0, sticky = "nsew", padx = 30, pady = 5)
    genderVar = StringVar(value = "MALE")
    genderFrame = Frame(inputFrame, bg = "grey")
    genderFrame.grid(row = 2, column = 1, sticky = "nsew", padx = 0, pady = 5)
    maleRadio = Radiobutton(genderFrame, text = "MALE", variable = genderVar, value = "MALE", font = "Arial 20", bg = "grey", fg = "white", command=updateGender)
    maleRadio.grid(row = 0, column = 0, sticky = "w", padx = 50, pady = 5)
    femaleRadio = Radiobutton(genderFrame, text = "FEMALE", variable = genderVar, value = "FEMALE", font = "Arial 20", bg = "grey", fg = "white", command=updateGender)
    femaleRadio.grid(row = 0, column = 1, sticky = "w", padx = 50, pady = 5)
    neutralRadio = Radiobutton(genderFrame, text = "NEUTRAL", variable = genderVar, value = "NEUTRAL", font = "Arial 20", bg = "grey", fg = "white", command=updateGender)
    neutralRadio.grid(row = 0, column = 2, sticky = "w", padx = 50, pady = 5)
    

    #Voice Selection
    voiceLabel = Label(inputFrame, text = "                Voice", bg = "grey", anchor = "e", fg = "white", font = 'arial 20')
    voiceLabel.grid(row = 3, column = 0, sticky = "nsew", padx = 30, pady = 5)
    voiceVar = StringVar(value = "text")
    availableVoices = availablevoices.getVoices(GOOGLE_FILE_PATH, language, engine, genderVar.get())
    voiceVar.set(availableVoices[0])
    voiceMenu = OptionMenu(inputFrame, voiceVar, *availableVoices, command=updateVoice)
    voiceMenu.config(font=('Arial', 20), bg='grey', fg='black', relief='solid',  bd=2, highlightthickness=0)
    voiceMenu['menu'].config(font=('Arial', 15), bg='#ffffff', fg='black', relief='solid', bd=0)
    voiceMenu.grid(row=3, column=1, sticky="nsew", padx=10, pady=10)
    voice = voiceVar.get()

    #Input Text Type
    textTypeLabel = Label(inputFrame, text = "            Text Type", bg = "grey", anchor = "e", fg = "white", font = 'arial 20')
    textTypeLabel.grid(row = 4, column = 0, sticky = "nsew", padx = 30, pady = 5)
    textTypeVar = StringVar(value = "text")
    textTypeFrame = Frame(inputFrame, bg = "grey")
    textTypeFrame.grid(row = 4, column = 1, sticky = "nsew", padx = 0, pady = 5)
    textRadio = Radiobutton(textTypeFrame, text = "Text        ", variable = textTypeVar, value = "text", font = "Arial 20", bg = "grey", fg = "white")
    textRadio.grid(row = 0, column = 0, sticky = "w", padx = 50, pady = 5)
    ssmlRadio = Radiobutton(textTypeFrame, text = "SSML    ", variable = textTypeVar, value = "ssml", font = "Arial 20", bg = "grey", fg = "white")
    ssmlRadio.grid(row = 0, column = 1, sticky = "w", padx = 50, pady = 5)

    #Text to be converted to speech
    mainTextLabel = Label(inputFrame, text = "Text", bg = "grey", anchor = "e", fg = "white", font = 'arial 20')
    mainTextLabel.grid(row = 5, column = 0, sticky = "nsew", padx = 30, pady = 5)
    mainText = Text(inputFrame, height = 10, width = 50, font = 'Arial 20', wrap = "word", bg = "white", fg = "black")
    mainText.grid(row = 5, column = 1, sticky = "nsew", padx = 30, pady = 5)
    mainText.config(borderwidth = 2, relief = "solid", highlightthickness = 0, bd = 0)

    #Submit button
    submitFrame = Frame(mainFrame, bg = "grey")
    submitFrame.grid(row = 4, column = 0, sticky = "nsew", pady = (10, 0))
    submitFrame.grid_columnconfigure(0, weight = 1)
    submitButton = Button(submitFrame, text = "Submit", font = "Arial 20", fg = "black", anchor = "center", command = playAudio)
    submitButton.pack(side = "bottom", pady = 5)
    submitButton.config(borderwidth = 2, relief = "solid", highlightthickness = 0, bd = 0)

    #Errors
    errorFrame = Frame(mainFrame, bg = "grey")
    errorFrame.grid(row = 5, column = 0, sticky = "nsew", pady = (10, 0))
    errorFrame.grid_columnconfigure(0, weight = 1)
    errorLabel = Label(errorFrame, text = "", anchor = "center", bg = "grey", fg = "#9D0000", font = "Arial 18")
    errorLabel.grid(row = 0, column = 0, sticky = "nsew", padx = 30, pady = 10)


    #Status - TO BE IMPLEMENTED IN A LATER ITERATION
    #statusLabel = Label(root, text = "Usage: ", anchor = "sw", bg = "yellow", fg = "#000000", font = "Arial 15")
    #statusLabel.grid(row = 6, column = 0, sticky = "nsew")
    #updateQuota()
    
    root.mainloop()


