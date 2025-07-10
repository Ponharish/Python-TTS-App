import sys
import os

def get_key_file_path(path):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, path)
    else:
        return os.path.join(os.path.dirname(__file__), path)
