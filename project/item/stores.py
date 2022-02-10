import django
django.setup()

from item.models import Item


def scrapingKabum(soup):
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
            return name, image, 0

    except:
        return errorNotFound()


def scrapingPontoDoNerd(soup):
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
            return name, image, 0

    except:
        return errorNotFound()
    
def scrapingDell(soup):
    try:
        name = soup.select_one('#cf-body > div.row.cf-hero-section > div.col.cf-hero-details > div.cf-product-order > h1 > span').text.strip()

        image = soup.find(
            'img', attrs={'data-testid': 'sharedPolarisHeroPdImage'}).get("src")

        try:
            price = soup.select_one('#cf-body > div.row.cf-hero-section > div.col.cf-hero-details > div.cf-hero-price > div > div.cf-i.cf-dell-price > div').text.strip().replace(".", "").replace("$", "").replace("R", "").strip()
            price = float(price.replace(",", "."))
            return name, image, price

        except:
            return name, image, 0

    except:
        return errorNotFound()

def errorNotFound():
    return "Erro ao encontrar o item", "https://www.thermaxglobal.com/wp-content/uploads/2020/05/image-not-found-300x169.jpg", None
