from tkinter import *
import tkinter.messagebox

from keymanagement import pathresolver

import json
import os

KEY_CONFIG_FILE = pathresolver.get_key_file_path('../.keys/.keyconfig.json')

def removeService(parent = None):
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
            
    def remove():
        service = serviceVar.get()

        answer = tkinter.messagebox.askquestion('Delete Config File', 'Are you sure you want to delete the file: '+ service)

        if answer == 'no':
            return     
        
        filePath = fetchPath(service)
        root.destroy()
        fullFilePath = pathresolver.get_key_file_path(filePath)
        
        os.remove(fullFilePath)

        services = []
        try: 
            with open(KEY_CONFIG_FILE, 'r') as f:
                services = json.load(f)
        except:
            pass

        services.remove(filePath)
        with open(KEY_CONFIG_FILE, 'w') as f:
            json.dump(services, f)
        
    
    def on_close():
        root.destroy()
        
    root = Toplevel(parent) if parent else Tk()
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

    services = ['']
    try: #to handle case where file is empty
        with open(KEY_CONFIG_FILE, 'r') as f:
            services = json.load(f)
            for i in range(0, len(services)):
                services[i] = services[i].split('.')[4]
    except Exception as e:
        pass
    if not services:
        services = ['']
    
    serviceFrame = Frame(mainFrame, bg = "grey")
    serviceFrame.grid(row = 1, column = 0, sticky = "nsew", pady = (0, 0))
    serviceFrame.grid_columnconfigure(1, weight = 1)
    
    chooseServLabel = Label(serviceFrame, text = "Select service to remove", bg = "grey", anchor = "e", fg = "white", font = 'arial 20')
    chooseServLabel.grid(row = 0, column = 0, sticky = "nsew", padx = 30, pady = 10)
    serviceVar = StringVar()
    serviceVar.set(services[0])
    serviceMenu = OptionMenu(serviceFrame, serviceVar, *services)
    serviceMenu.config(font=('Arial', 20), bg='grey', fg='black', relief='solid', bd=2, highlightthickness=0)
    serviceMenu['menu'].config(font=('Arial', 15), bg='#ffffff', fg='black', relief='solid', bd=0)
    serviceMenu.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    if serviceVar.get() == '': #should not reach here
        serviceVar.set("No existing services found")
        serviceMenu['menu'].delete(0, 'end')

    #Next button
    nextFrame = Frame(mainFrame, bg = "grey")
    nextFrame.grid(row = 2, column = 0, sticky = "nsew", pady = (10, 0))
    nextFrame.grid_columnconfigure(0, weight = 1)
    nextButton = Button(nextFrame, text = "Remove", font = "Arial 20", bg = "blue", fg = "black", anchor = "center", command = remove)
    nextButton.pack(side = "bottom", pady = 5)
    nextButton.config(borderwidth = 2, relief = "solid", highlightthickness = 0, bd = 0)

    parent.wait_window(root)
