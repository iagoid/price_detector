import urllib.request
import datetime
from bs4 import BeautifulSoup
from django.db.models import Q

from .models import Item
import time

def verifyItemsToScraping():
    print("=========== EXECUTANDO SCRAPING")

    minutes = datetime.timedelta(minutes=15)
    fifteen_minutes_ago = datetime.datetime.now().astimezone() - minutes
    items = Item.objects.all().filter(
        Q(updated_at__lt=(fifteen_minutes_ago)) | Q(name=None))

    for i in range(len(items)):

        page = urllib.request.urlopen(items[i].link)
        soup = BeautifulSoup(page, 'html5lib')

        if "kabum.com.br" in items[i].link:
            items[i].name, items[i].image, items[i].price = scrapingKabum(
                soup, items[i])
        elif "pontodonerd.com.br" in items[i].link:
            items[i].name, items[i].image, items[i].price = scrapingPontoDoNerd(
                soup, items[i])
        else:
            print("Seu link não é de uma loja conhecida")

        items[i].save()
        time.sleep(0.5)


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
