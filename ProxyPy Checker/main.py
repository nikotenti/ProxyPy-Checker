from Core.scraper_proxy import *
from Core.proxy_checker import *
from Core.menu import *
from termcolor import colored

import sys

def Main():
    try:
        Clear()
        Banner()
        Main_Menu()
    except KeyboardInterrupt:
        print(colored("\nExiting...", 'yellow'))
        sys.exit()

if __name__ == '__main__':
    Main()