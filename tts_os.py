import io
import pygame
import pyttsx3

from tkinter import *
from tkinter import filedialog

from ostts import availablelanguages
from ostts import availablevoices

from keymanagement import changeservice
from keymanagement import keymanagement
from keymanagement import register


from audiomanager import playaudio

OSTTS_FILE_PATH = ".os_config.txt"

def startAppGui():
    def reconfigureKeys(): 
        root.destroy()
        changeservice.changeService()
    
    def reconfigureVoice(*args):
        language = languageVar.get()
        language = language.split(' - ')[0] 
        availableVoices = availablevoices.getVoices(language)
        voiceVar.set(availableVoices[0])
        voiceMenu['menu'].delete(0, 'end')
        for voice in availableVoices:
            voiceMenu['menu'].add_command(label=voice, command=lambda value=voice: (voiceVar.set(value), updateVoice()))
                   
    def updateLanguage(*args):
        reconfigureVoice()
        
    def updateVoice(*args):
        #nothing to be done at the moment
        pass
    
        
    def playAudio():
        errorLabel.config(text = "")
        text = mainText.get("1.0", "end-1c")
        print(voiceVar.get())
        print()
        choosenVoice = voiceVar.get()
        language = languageVar.get()
        language = language.split(' - ')[0]   

        if len(text) > 990: #In future iteration, improve this by splitting the request into chunks and processing
           errorLabel.config(text = "The input provided is too long")
           return
        elif len(text)  ==  0:
           errorLabel.config(text = "Provide an Input text")
           return

        try:
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            selectedVoice = None
            for voice in voices:
                if language in voice.languages and choosenVoice.lower() in voice.name.lower():
                    selectedVoice = voice
                    break

            if selectedVoice:
                engine.setProperty('voice', selectedVoice.id)

            filePath = None
            if not filePath:
                filePath = filedialog.asksaveasfilename(
                    defaultextension=".wav",  
                    filetypes=[("WAV files", "*.wav"), ("MP3 files", "*.mp3"), ("All files", "*.*")],
                    title="Save Audio File"
                )
            if not filePath:
                return
            engine.save_to_file(text, filePath)
            engine.runAndWait() 

        except Exception as e:
            errorLabel.config(text = "An error has occured")
            return



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

    reconfigureKeysButton = Button(credentialsFrame, text = "Change Service", font = "Arial 20", bg = "blue", fg = "black", anchor = "center", command = reconfigureKeys)
    reconfigureKeysButton.grid(row = 0, column = 0, sticky = "nsew", padx = 30, pady = 10)
    reconfigureKeysButton.config(borderwidth = 2, relief = "solid", highlightthickness = 0, bd = 0)
    KeyLabel = Label(credentialsFrame, text = "OS Native TTS engine loaded", bg = "grey", anchor = "w", fg = "white", font = 'arial 20')
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
    languages = availablelanguages.getLanguages()   
    if 'en_US - English' in languages:
        languages.remove('en_US - English')
        languages.insert(0, 'en_US - English')
    languageVar.set(languages[0])
    languageMenu = OptionMenu(inputFrame, languageVar, *languages, command=updateLanguage)
    languageMenu.config(font=('Arial', 20), bg='grey', fg='black', relief='solid',  bd=2, highlightthickness=0)
    languageMenu['menu'].config(font=('Arial', 15), bg='#ffffff', fg='black', relief='solid', bd=0)
    languageMenu.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    language = languageVar.get()
    language = language.split(' - ')[0]

    #Voice Selection
    voiceLabel = Label(inputFrame, text = "                Voice", bg = "grey", anchor = "e", fg = "white", font = 'arial 20')
    voiceLabel.grid(row = 1, column = 0, sticky = "nsew", padx = 30, pady = 5)
    voiceVar = StringVar(value = "text")
    availableVoices = availablevoices.getVoices(language)
    voiceVar.set(availableVoices[0])
    voiceMenu = OptionMenu(inputFrame, voiceVar, *availableVoices, command=updateVoice)
    voiceMenu.config(font=('Arial', 20), bg='grey', fg='black', relief='solid',  bd=2, highlightthickness=0)
    voiceMenu['menu'].config(font=('Arial', 15), bg='#ffffff', fg='black', relief='solid', bd=0)
    voiceMenu.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
    voice = voiceVar.get()

    #Text to be converted to speech
    mainTextLabel = Label(inputFrame, text = "Text", bg = "grey", anchor = "e", fg = "white", font = 'arial 20')
    mainTextLabel.grid(row = 2, column = 0, sticky = "nsew", padx = 30, pady = 5)
    mainText = Text(inputFrame, height = 10, width = 50, font = 'Arial 20', wrap = "word", bg = "white", fg = "black")
    mainText.grid(row = 2, column = 1, sticky = "nsew", padx = 30, pady = 5)
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
