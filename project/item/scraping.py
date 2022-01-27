# importe a biblioteca usada para consultar uma URL
import urllib.request
from datetime import datetime, timedelta
# importe as funções BeautifulSoup para analisar os dados retornados do site
from bs4 import BeautifulSoup

from .models import Item
import time

def verifyItemsToScraping():
    items = Item.objects.all().order_by(
        'updated_at')

    for i in range(len(items)):

        updated_at = items[i].updated_at.date()
        now = datetime.utcnow().date()

        if now != updated_at or items[i].name is None:

            page = urllib.request.urlopen(items[i].link)
            soup = BeautifulSoup(page, 'html5lib')

            if "kabum.com.br" in items[i].link:
                items[i].name, items[i].image, items[i].price = scrapingKabum(soup, items[i])
            # if "magazineluiza.com.br" in items[i].link:
            #     items[i].name, items[i].image, items[i].price = scrapingMagazindeLuiza(soup)
            

            items[i].save()
            time.sleep(1)

        else:
            return

# O scraping do Magazine Luiza não funciona
# def scrapingMagazindeLuiza(soup):
#     # try:
#         name = soup.find('h1', attrs={'class': 'header-product__title'}).text.strip()
#         image = soup.find(
#                     'img', attrs={'class': 'showcase-product__big-img'}).get("src")
#         price = soup.find(
#                     'span', attrs={'class': 'price-template__text'}).text.replace(".", "").strip()
#         price = float(price.replace(",", "."))
#         return name, image, price

    # except:
    #     return "Erro ao encontrar o item ", "https://www.thermaxglobal.com/wp-content/uploads/2020/05/image-not-found-300x169.jpg", 0



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
            name = "Produto indisponivel"
            
            return "Indisponível: "+ name, image, 0

    except:
        return "Erro ao encontrar o item ", "https://www.thermaxglobal.com/wp-content/uploads/2020/05/image-not-found-300x169.jpg", 0