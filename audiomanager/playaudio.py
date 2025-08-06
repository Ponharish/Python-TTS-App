from tkinter import ttk, filedialog
from tkinter import *

from mutagen.mp3 import MP3

import io
import os
import pygame
import time

playbackWindowRef = None
afterId = None
elapsedLabel = None

def playAudio(audioBytes, root):
    global volume, isPlaying, userDragging, startTime, pausedTime, seekOffset, playbackWindowRef, afterId, elapsedLabel
    
    if playbackWindowRef:
        try:
            playbackWindowRef.destroy()
            playbackWindowRef = None
        except:
            playbackWindowRef = None
        
    volume = 0.5
    isPlaying = False

    userDragging = False
    startTime = 0.0
    pausedTime = 0.0
    seekOffset = 0.0

    afterId = None


    def initAudio(audioBytes):
        global startTime, seekOffset, isPlaying, pausedTime
        
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(io.BytesIO(audioBytes))
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(0)
        startTime = time.time()
        pygame.mixer.music.pause() 
        pausedTime = time.time()
        seekOffset = 0.0
        isPlaying = False

        updateElapsedTime()


    def setVolume(vol):
        volume = float(vol)
        pygame.mixer.music.set_volume(volume)

    def updateElapsedTime():
        global startTime, pausedTime, isPlaying, afterId
        
        if not elapsedLabel.winfo_exists():
            try:
                elapsedLabel.after_cancel(after_id)
            except Exception as e:
                pass
    
        if isPlaying and not userDragging:
            elapsed = time.time() - startTime
            if elapsed >= audioDuration:
                pygame.mixer.music.stop()
                pygame.mixer.music.play(0, 0)
                isPlaying = False
                startTime = time.time()
                pygame.mixer.music.pause() 
                pausedTime = time.time()
                seekSlider.set(0)
                elapsedLabel.config(text="00:00")
                togglePauseButton.config(text="Play")
            else:
                seekSlider.set(elapsed)
                minutes = int(elapsed) // 60
                seconds = int(elapsed) % 60
                elapsedLabel.config(text=f"{minutes:02}:{seconds:02}")

        afterId = elapsedLabel.after(1000, updateElapsedTime)


    def togglePause():
        global isPlaying, pausedTime, startTime
        
        if not isPlaying:
            pygame.mixer.music.unpause()
            startTime += time.time() - pausedTime #this effectively manipulates the start time based on when it was paused
            isPlaying = True
            togglePauseButton.config(text="Pause")
        else:
            pygame.mixer.music.pause()
            pausedTime = time.time()
            isPlaying = False
            togglePauseButton.config(text="Play")

    def resetElapsed():
        elapsedLabel.config(text=f"00:00")

    def replay():
        global startTime
        pygame.mixer.music.play(0, 0)
        if not isPlaying:
            pygame.mixer.music.pause()
        startTime = time.time()
        resetElapsed()
        seekSlider.set(0)

    def download():
        filePath = None
        filePath = filedialog.asksaveasfilename(
            defaultextension=".wav",  
            filetypes=[("MP3 files", "*.mp3")],
            title="Save Audio File"
        )
        if not filePath:
            return
        try:
            with open(filePath, "wb") as f:
                f.write(audioBytes)
        except Exception as e:
            errorLabel.config(text = "Unable to save the file. Try again later")  

    def start_seek(event):
        global userDragging
        userDragging = True

    def stop_seek(event):
        global userDragging, startTime
        userDragging = False
        newTime = float(seekSlider.get())
        pygame.mixer.music.play(0, newTime)
        if not isPlaying:
            pygame.mixer.music.pause()
            minutes = int(newTime) // 60
            seconds = int(newTime) % 60
            elapsedLabel.config(text=f"{minutes:02}:{seconds:02}")
        startTime = time.time() - newTime  

    def onPlaybackWindowClose():
        global afterId, playbackWindowRef
        if afterId:
            try:
                elapsedLabel.after_cancel(afterId)
            except Exception:
                pass
            afterId = None
        pygame.mixer.music.stop()
        if playbackWindowRef:
            playbackWindowRef.destroy()
            playbackWindowRef = None 


    #GUI
    playbackWindow = Toplevel(root)
    playbackWindowRef = playbackWindow
    playbackWindow.title("Audio Playback")
    playbackWindow.minsize(width = 800, height = 350)
    playbackWindow.grid_rowconfigure(0, weight = 1)
    playbackWindow.grid_columnconfigure(0, weight = 1)


    mainFrame = Frame(playbackWindow, width = 700, height = 370, bg = "grey")
    mainFrame.grid(row = 0, column = 0, sticky = "nsew")
    mainFrame.grid_columnconfigure(1, weight = 1)
        

    headerLabel = Label(mainFrame, text = "Audio Playback", bg = "grey", anchor = "center", fg = "white", font = 'arial 29')
    headerLabel.grid(row = 0, column = 1, sticky = "nsew", pady = 15)

    # Control Buttons
    togglePauseButton = Button(mainFrame, text = "Play", fg = "black", font = "Arial 20", command = togglePause)
    togglePauseButton.grid(row = 1, column = 1, sticky = "nsew", padx = 200, pady = 10)
    togglePauseButton.config(borderwidth = 2, relief = "solid", highlightthickness = 0, bd = 0)

    replayButton = Button(mainFrame, text = "Replay", fg = "black", font = "Arial 20",  command = replay)
    replayButton.grid(row = 2, column = 1, sticky = "nsew", padx = 200, pady = 10)
    replayButton.config(borderwidth = 2, relief = "solid", highlightthickness = 0, bd = 0)

    downloadButton = Button(mainFrame, text = "Download Audio", fg = "black", font = "Arial 20",  command = download)
    downloadButton.grid(row = 3, column = 1, sticky = "nsew", padx = 200, pady = 10)
    downloadButton.config(borderwidth = 2, relief = "solid", highlightthickness = 0, bd = 0)


    #Volume
    volumeFrame = Frame(mainFrame, bg = "grey")
    volumeFrame.grid(row = 4, column = 1, sticky = "nsew", padx = 200, pady = 20)
    volumeFrame.grid_columnconfigure(1, weight = 1)

    VolumeLabel = Label(volumeFrame, text = "Volume", bg = "grey", anchor = "center", fg = "white", font = 'arial 18')
    VolumeLabel.grid(row = 0, column = 0, sticky = "nsew")

    volumeSlider = ttk.Scale(volumeFrame, from_ = 0, to = 1, value = volume, orient = "horizontal", command = setVolume)
    volumeSlider.grid(row = 0, column = 1, sticky = "nsew", padx = 7)
    

    # Audio Seek and elapsed time display
    audio = MP3(io.BytesIO(audioBytes))
    audioDuration = audio.info.length
    totalMinutes = int(audioDuration // 60)
    totalSeconds = int(audioDuration % 60)

    elapsedLabel = Label(mainFrame, text = "00:00", bg = "grey", anchor = "center", fg = "white", font = 'arial 18')
    elapsedLabel.grid(row = 5, column = 0, sticky = "nsew", padx = 5)

    seekSlider = ttk.Scale(mainFrame, from_ = 0, to = audioDuration, orient = "horizontal")
    seekSlider.grid(row = 5, column = 1, sticky = "nsew", padx = 10, pady = 20)

    seekSlider.bind("<ButtonPress-1>", start_seek)
    seekSlider.bind("<ButtonRelease-1>", stop_seek)

    totalTimeLabel = Label(mainFrame, text = f"{totalMinutes:02}:{totalSeconds:02}", bg = "grey", anchor = "center", fg = "white", font = 'arial 18')
    totalTimeLabel.grid(row = 5, column = 2, sticky = "nsew", padx = 5)
    

    #Errors
    errorFrame = Frame(mainFrame, bg = "grey")
    errorFrame.grid(row = 6, column = 0, sticky = "nsew", pady = (10, 0))
    errorFrame.grid_columnconfigure(0, weight = 1)
    errorLabel = Label(errorFrame, text = "", anchor = "center", bg = "grey", fg = "#9D0000", font = "Arial 15")
    errorLabel.grid(row = 0, column = 0, sticky = "nsew", padx = 10, pady = 10)

    initAudio(audioBytes)
    playbackWindow.protocol("WM_DELETE_WINDOW", onPlaybackWindowClose)
    root.wait_window(playbackWindow)

def stopMusic():
    global afterId, elapsedLabel
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
    try:
        elapsedLabel.after_cancel(afterId)
    except:
        pass
    afterId = None
