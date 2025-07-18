from keymanagement import selectservice
from keymanagement import createconfig

from util import checkconnection

import os

def main():
    if not checkconnection.checkConnection():
        return
    createconfig.createConfig()
    selectservice.selectService()

main()
