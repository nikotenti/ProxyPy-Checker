import requests
from bs4 import BeautifulSoup
from termcolor import colored

proxyList = []

def makesoup(url):
    page=requests.get(url)
    return BeautifulSoup(page.text,"html.parser")

def proxyscrape(table, limit):

    global proxyList
    
    if int(limit) > 0:
        current_limit = 0
        for row in table.findAll('tr'):
            if current_limit < int(limit):
                current_limit += 1
                fields = row.findAll('td')
                count = 0
                proxy = ""
                for cell in row.findAll('td'):
                    if count == 1:
                        proxy += ":" + cell.text.replace('&nbsp;', '')
                        proxyList.append(proxy)
                        #print(proxy)
                        break
                    proxy += cell.text.replace('&nbsp;', '')
                    count += 1
            elif current_limit == int(limit):
                break
    else:
        for row in table.findAll('tr'):
            fields = row.findAll('td')
            count = 0
            proxy = ""
            for cell in row.findAll('td'):
                if count == 1:
                    proxy += ":" + cell.text.replace('&nbsp;', '')
                    proxyList.append(proxy)
                    #print(proxy)
                    break
                proxy += cell.text.replace('&nbsp;', '')
                count += 1
    
def scrapeproxies(url, limit):
    global proxyList

    soup=makesoup(url)
    table = soup.find('table', attrs={'id': 'proxylisttable'}) #, attrs={'id': 'proxylisttable'}
    proxyscrape(table, limit)
    return proxyList
