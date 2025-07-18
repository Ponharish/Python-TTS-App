from keymanagement import pathresolver

import json
import os

def createConfig():
    folder_name = "../.keys"
    folder_path = pathresolver.get_key_file_path(folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        
    KEY_CONFIG_FILE = pathresolver.get_key_file_path('../.keys/.keyconfig.json')
    if not os.path.exists(KEY_CONFIG_FILE):
        services = []
        
        with open(KEY_CONFIG_FILE, 'w') as f:
            json.dump(services, f)
