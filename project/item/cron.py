import kronos
from item.scraping import verifyItemsToScraping

@kronos.register('* * * * *')
def scrappingRotine():
    verifyItemsToScraping()