import schedule
from django.shortcuts import render

from .models import Item
from .scraping import verifyItemsToScraping


def itemsList(request):
    verifyItemsToScraping()

    items = Item.objects.exclude(price=0).order_by('-price')
    unavailableItems  = Item.objects.filter(price=0).order_by('-price')



    # items = Item.objects.order_by(F('price').asc(nulls_last=True))


    context = {
        'items': items,
        'unavailableItems': unavailableItems,
        }

    return render(request, 'items/list.html', context)
