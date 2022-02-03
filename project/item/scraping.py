import urllib.request
import datetime
from bs4 import BeautifulSoup
from django.db.models import Q
import multiprocessing
import time
import django
django.setup()

from item.models import Item

def repeaterItemsToScraping():
    while(1):
        p =  multiprocessing.Process(target= verifyItemsToScraping)
        p.start()
        p.join()
        time.sleep(300)

def verifyItemsToScraping():
    print("=========== EXECUTANDO SCRAPING")

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

def getSite(item):
    page = urllib.request.urlopen(item.link)
    soup = BeautifulSoup(page, 'html5lib')

    if "kabum.com.br" in item.link:
        item.name, item.image, item.price = scrapingKabum(
            soup, item)
    elif "pontodonerd.com.br" in item.link:
        item.name, item.image, item.price = scrapingPontoDoNerd(
            soup, item)
    else:
        print("Seu link não é de uma loja conhecida")

    item.save()

def scrapingKabum(soup, item):
    try:
        name = soup.find('h1', attrs={'itemprop': 'name'}).text.strip()
        image = soup.find(
            'img', attrs={'class': 'iiz__img'}).get("src")

        try:
            price = soup.find(
                'h4', attrs={'class': 'finalPrice'}).text.replace(".", "").replace("$", "").replace("R", "").strip()
            price = float(price.replace(",", "."))
            return name, image, price

        except:
            soup.find('div', attrs={'id': 'formularioProdutoIndisponivel'})
            return "Indisponível: " + name, image, 0

    except:
        return "Erro ao encontrar o item ", "https://www.thermaxglobal.com/wp-content/uploads/2020/05/image-not-found-300x169.jpg", 0


def scrapingPontoDoNerd(soup, item):
    try:
        name = soup.find(
            'h1', attrs={'class': 'nome-produto titulo cor-secundaria'}).text.strip()
        image = soup.find(
            'img', attrs={'id': 'imagemProduto'}).get("src")

        try:
            price = soup.find(
                'strong', attrs={'class': 'preco-promocional cor-principal'}).text.replace(".", "").replace("$", "").replace("R", "").strip()
            price = float(price.replace(",", "."))
            return name, image, price

        except:
            return "Indisponível: " + name, image, 0

    except:
        return "Erro ao encontrar o item ", "https://www.thermaxglobal.com/wp-content/uploads/2020/05/image-not-found-300x169.jpg", 0
