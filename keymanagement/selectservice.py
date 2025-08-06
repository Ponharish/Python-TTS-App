import json

import tts_aws
import tts_google

import tkinter.messagebox
from tkinter import *

from keymanagement import pathresolver
from keymanagement import register
from keymanagement import removeservice


KEY_CONFIG_FILE = pathresolver.get_key_file_path('../.keys/.keyconfig.json')

def selectService():

    def fetchPath(file):
        services = ['']
        try: #to handle case where file is empty
            with open(KEY_CONFIG_FILE, 'r') as f:
                services = json.load(f)
        except:
            pass
        for i in services:
            if file in i:
                return i
        
    def addService():
        root.withdraw()
        register.registerKey(root)
        root.deiconify()
        reconfigureServices()

    def deleteService():
        root.withdraw()
        removeservice.removeService(root)
        root.deiconify()
        reconfigureServices()
    
    def selectService():
        service = serviceVar.get()
        filePath = fetchPath(service)
        root.destroy()
        filePath = pathresolver.get_key_file_path(filePath)
        if "AWS" in service:
            tts_aws.startAppGui(filePath)
        else:
            tts_google.startAppGui(filePath)

    def reconfigureServices(*args):
        services = ['']
        try: #to handle case where file is empty
            with open(KEY_CONFIG_FILE, 'r') as f:
                services = json.load(f)
                for i in range(0, len(services)):
                    services[i] = services[i].split('.')[4]
        except:
            pass
        if not services:
            services = ['']

        if services[0] != '':
            serviceVar.set(services[0])
        else:
            serviceVar.set("No existing services found")
        serviceMenu['menu'].delete(0, 'end')
        if services[0] != '':
            for svc in services:
                serviceMenu['menu'].add_command(label=svc, command=lambda value=svc: (serviceVar.set(value)))
        if services[0] == '':
            rmserviceFrame.grid_remove()
            nextFrame.grid_remove()
        else:
            rmserviceFrame.grid()
            nextFrame.grid()
            
        
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

    headerLabel = Label(headerFrame, text = "Python TTS App", bg = "grey", anchor = "center", fg = "white", font = 'arial 39')
    headerLabel.grid(row = 0, column = 0, sticky = "nsew")

    services = []
    try: #to handle case where file is empty
        with open(KEY_CONFIG_FILE, 'r') as f:
            services = json.load(f)
            for i in range(0, len(services)):
                services[i] = services[i].split('.')[4]
    except:
        pass
    if not services:
        services = ['']

    serviceFrame = Frame(mainFrame, bg = "grey")
    serviceFrame.grid(row = 1, column = 0, sticky = "nsew", pady = (0, 0))
    serviceFrame.grid_columnconfigure(1, weight = 1)
    
    chooseServLabel = Label(serviceFrame, text = "Select service", bg = "grey", anchor = "e", fg = "white", font = 'arial 20')
    chooseServLabel.grid(row = 0, column = 0, sticky = "nsew", padx = 30, pady = 10)
    serviceVar = StringVar()
    serviceVar.set(services[0]) 
    serviceMenu = OptionMenu(serviceFrame, serviceVar, *services)
    serviceMenu.config(font=('Arial', 20), bg='grey', fg='black', relief='solid', bd=2, highlightthickness=0)
    serviceMenu['menu'].config(font=('Arial', 15), bg='#ffffff', fg='black', relief='solid', bd=0)
    serviceMenu.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    if serviceVar.get() == '':
        serviceVar.set("No existing services found")
        serviceMenu['menu'].delete(0, 'end')

    #Next button
    nextFrame = Frame(mainFrame, bg = "grey")
    nextFrame.grid(row = 2, column = 0, sticky = "nsew", pady = (10, 0))
    nextFrame.grid_columnconfigure(0, weight = 1)
    nextButton = Button(nextFrame, text = "Next", font = "Arial 20", fg = "black", anchor = "center", command = selectService)
    nextButton.pack(side = "bottom", pady = 5)
    nextButton.config(borderwidth = 2, relief = "solid", highlightthickness = 0, bd = 0)

    #Add new service button
    newserviceFrame = Frame(mainFrame, bg = "grey")
    newserviceFrame.grid(row = 3, column = 0, sticky = "nsew", pady = (10, 0))
    newserviceFrame.grid_columnconfigure(0, weight = 1)
    newserviceButton = Button(newserviceFrame, text = "Add Service", font = "Arial 20", fg = "black", anchor = "center", command = addService)
    newserviceButton.pack(side = "bottom", pady = 5)
    newserviceButton.config(borderwidth = 2, relief = "solid", highlightthickness = 0, bd = 0)

    #remove service button
    rmserviceFrame = Frame(mainFrame, bg = "grey")
    rmserviceFrame.grid(row = 4, column = 0, sticky = "nsew", pady = (10, 0))
    rmserviceFrame.grid_columnconfigure(0, weight = 1)
    rmserviceButton= Button(rmserviceFrame, text = "Delete Service", font = "Arial 20", fg = "black", anchor = "center", command = deleteService)
    rmserviceButton.pack(side = "bottom", pady = 5)
    rmserviceButton.config(borderwidth = 2, relief = "solid", highlightthickness = 0, bd = 0)

    if serviceVar.get() == 'No existing services found':
        rmserviceFrame.grid_remove()
        nextFrame.grid_remove()

    root.mainloop()



