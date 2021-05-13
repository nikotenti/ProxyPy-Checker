import pyfiglet, os
from termcolor import colored
from Core.scraper_proxy import *
from Core.proxy_checker import *

def Main_Menu():
    dashboard = input(colored('\n[1] Scraping proxies online - [2] Import proxies from file: ', 'blue'))
    if dashboard == '1':
        thrd = input(colored('\nHow many threads(racomanded 50): ', 'blue'))
        limit = input(colored('\nHow many proxy do you want scraping for sites? (0 = All): ', 'blue'))
        print('')
        Checking_Proxy_Sites()
        Scrape_Online(thrd, limit)
    elif dashboard == '2':
        path = input(colored('\nFile path: ', 'blue'))
        thrd = input(colored('\nHow many threads(racomanded 50): ', 'blue'))
        Scrape_From_File(path, thrd)
    else:
        print(colored('invalid command', 'red'))
        Main_Menu()

def Banner():
    result = pyfiglet.figlet_format("ProxyPy Checker")

    banner = colored(result, 'red') + '\n\n'
    print(banner)

def Clear():
    if os.name == 'nt':
        os.system('cls')
    if os.name == "posix":
        os.system('clear')

    