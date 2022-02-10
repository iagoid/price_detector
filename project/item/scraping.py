import urllib.request
import datetime
from bs4 import BeautifulSoup
from django.db.models import Q
import multiprocessing
from selenium import webdriver
import time
import django
from django.contrib import messages

django.setup()

from item.models import Item
from item.stores import scrapingKabum, scrapingDell, scrapingPontoDoNerd

# Realiza o loop de chamar a função que faz o webscraping após determinado tempo
def repeaterItemsToScraping():
    while(1):
        p =  multiprocessing.Process(target= verifyItemsToScraping)
        p.start()
        p.join()
        time.sleep(300)

# Verifica qual item deve ser novamente buscado
def verifyItemsToScraping():
    print("=========== EXECUTANDO SCRAPING", datetime.datetime.now())

    minutes = datetime.timedelta(minutes=15)
    fifteen_minutes_ago = datetime.datetime.now().astimezone() - minutes
    items = Item.objects.all().filter(
        Q(updated_at__lt=(fifteen_minutes_ago)) | Q(name=None))

    process_list = []
    for i in range(len(items)):
        p =  multiprocessing.Process(target= getSite, args=(items[i], ))
        p.start()
        process_list.append(p)
        time.sleep(0.25)
    
    for process in process_list:
        process.join()

# Manda as requisições para o site
def sendRequestToSite(link):
    browser = webdriver.PhantomJS(executable_path = '..\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
    browser.get(link)
    time.sleep(1)
    page = browser.page_source
    
    soup = BeautifulSoup(page, 'html5lib')
    return soup

# Verifica a URL em busca dos sites disponíveis e faz a solicitação para o site
def getSite(item):
    try:        
        soup = sendRequestToSite(item.link)
        item = verifySite(soup, item)
        
        if item.name != None or item.price != None:
            item.save()
            print('Criado com sucesso.')
                    
        else:
           print('Erro ao criar', item.url)
        
    except:
        print("URL INVÁLIDA " + item.link)

def verifySite(soup, item):
    if "kabum.com.br" in item.link:
            item.name, item.image, item.price = scrapingKabum(
                soup)
    elif "pontodonerd.com.br" in item.link:
        item.name, item.image, item.price = scrapingPontoDoNerd(
            soup)
    elif "dell.com" in item.link:
        item.name, item.image, item.price = scrapingDell(
            soup)
        
    return item
    