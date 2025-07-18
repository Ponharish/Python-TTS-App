from keymanagement import selectservice
from keymanagement import createconfig

import os

def main():
    createconfig.createConfig()
    selectservice.selectService()

main()
