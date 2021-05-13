from Core.scraper_proxy import *
from multiprocessing import Pool
from termcolor import colored
import requests
import time
from datetime import timedelta, date, datetime
import sys, os

URLS = []
Good_proxyList = []

def Requests_Proxy(proxy, attempt):

    try:
        proxies = {
            "http": "http://" + proxy,
            "https": "http://" + proxy,
            }

        r = requests.get("https://www.google.com/", proxies=proxies, timeout=15) # Get Proxy connections | https://api.ipify.org?format=json
        #jr = json.loads(r.text)
        if r.status_code == 200:
            print(colored('Attempt ' + str(attempt) + ' |', 'blue'), colored(proxy + ' ---> Response: ' + str(r.status_code), 'green'))
            return proxy
        elif r.status_code == 429:
            print(colored('Attempt ' + str(attempt) + ' |', 'blue'), colored(proxy + " Error: Too much requests", 'red' ))
        else:
            print(colored('Attempt ' + str(attempt) + ' |', 'blue'), colored(proxy + " Error: Connection Error", 'red' ))
    except requests.exceptions.ConnectTimeout as err:
        print(colored('Attempt ' + str(attempt) + ' |', 'blue'), colored(proxy + " Error: Connection Timeout", 'red' ))
        return 'None'
    except requests.exceptions.ConnectionError as err:
        print(colored('Attempt ' + str(attempt) + ' |', 'blue'), colored(proxy + " Error: Connection Error", 'red' ))
        return 'None'
    except requests.exceptions.RequestException as err:
        print("Request error")
        return 'None'
    except KeyboardInterrupt:
        raise KeyboardInterruptError()

def function_wrapper(args):
    return Requests_Proxy(*args)

def Run(data, thrd):
    global Good_proxyList
    starttime = time.time()
    p = Pool(processes=int(thrd))
    on = 0

    try:
        print(colored('Starting checking proxies connections\n', 'yellow'))
        result = p.map(function_wrapper, data)
        for line in result:
            if line != 'None':
                if line not in Good_proxyList:
                    Good_proxyList.append(line)
        p.close()
        print(colored('\n---- Checking complete ----', 'green'))
        endtime = time.time()
        total_time = endtime - starttime
        print(colored("\nElapsed time: " + str(timedelta(seconds=total_time)), 'yellow'))
        saving = input('\nDo you want save report? (No/yes): ')
        if 'yes' in saving or 'y' in saving:
            Save_Path(Good_proxyList)
        Good_proxyList = []
    except KeyboardInterrupt:
        print(colored('Kill threads, wait a few moment please...', 'yellow'))
        p.terminate()
    except Exception as e:
        p.terminate()
        print(colored('Exiting...', 'yellow'))
    finally:
        p.join()

def Scrape_Online(thrd, limit):
    attempt = 0
    data = []
    
    print(colored('---- Scraping Sites ----\n', 'yellow'))
    try:
        f = open('Config/proxies_sites.txt', 'r')
        Lines = f.readlines()
        for line in Lines:
            URLS.append(line.strip())
        for url in URLS:
            for proxy in scrapeproxies(url, limit):
                attempt += 1
                data.append((proxy, attempt))
            print(colored(url + ' scraped ', 'yellow'), colored('successfully', 'green'))
    except:
        print(colored(url + ' scraped ', 'yellow'), colored('failed', 'red'))
    print('')

    try:
        Run(data, thrd)
    except KeyboardInterrupt:
        raise KeyboardInterruptError()

def Scrape_From_File(path, thrd):
    attempt = 0
    data = []
    
    if path != '':
        try:
            with open(path) as file:
                for line in file:
                    attempt += 1
                    data.append((line.strip(), attempt))
            print(colored('Proxies loaded successfully', 'yellow'))
            try:
                Run(data, thrd)
            except Exception as e:
                print("Error: " + e)
            except KeyboardInterrupt:
                raise KeyboardInterruptError()
        except:
            print("File doesn't exist")
    else:
        print('File not exists')

def Checking_Proxy_Sites():
    print(colored('\n---- Checking Proxy Sites ----\n', 'yellow'))
    f = open('Config/proxies_sites.txt', 'r')
    lines = f.readlines()
    f.close()
    new_config = open("Config/proxies_sites.txt", "w")
    for line in lines:
        try:
            result = scrapeproxies(line.strip(), 2)
            if result != []:
                new_config.write(line)
                print(colored(line.strip() + ' Compatibile', 'green'))
            else:
                print(colored(line.strip() + ' Non compatibile  ---> Remove from file', 'red'))
        except:
            print(colored(line.strip() + ' Non compatibile  ---> Remove from file', 'red'))
    new_config.close()
    print(colored('\n---- Checking ended ----\n','yellow'))

def Save_Path(proxy_list):

    date_time = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
    path = f"output/{date_time}.txt"

    if os.path.exists('output') == False:
        os.mkdir('output')
    
    f = open(str(path), 'a')
    for proxy in proxy_list:
        f.write(str(proxy)+'\n')
    f.close()

    print(colored('\nReport file saved in --> ' + path, 'yellow'))
