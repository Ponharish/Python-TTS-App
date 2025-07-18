import socket
import tkinter.messagebox

def checkConnection():
    host="8.8.8.8"
    port=53
    timeout=15
    
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        tkinter.messagebox.showinfo("Python TTS", "There is no internet connection. Please connect to internet and try again")
        return False

