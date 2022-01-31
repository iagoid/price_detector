import urllib.request
from datetime import datetime
from bs4 import BeautifulSoup

from .models import Item
import time

def verifyItemsToScraping():
    print("============")
    items = Item.objects.all().order_by(
        'updated_at')

    for i in range(len(items)):

        updated_at = items[i].updated_at.date()
        now = datetime.utcnow().date()

        if now != updated_at or items[i].name is None:

            page = urllib.request.urlopen(items[i].link)
            soup = BeautifulSoup(page, 'html5lib')

            if "kabum.com.br" in items[i].link:
                items[i].name, items[i].image, items[i].price = scrapingKabum(
                    soup, items[i])
            elif "pontodonerd.com.br" in items[i].link:
                items[i].name, items[i].image, items[i].price = scrapingPontoDoNerd(
                    soup, items[i])
            # elif "magazineluiza.com.br" in items[i].link:
            #     items[i].name, items[i].image, items[i].price = scrapingMagazindeLuiza(soup)
            else:
                print("Seu link não é de uma loja conhecida")

            items[i].save()
            time.sleep(3)

        # este else será utilizado nos casos onde os items estão ordenado por updated_at crescente
        # else:
        #     return

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
