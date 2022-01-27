import schedule
from django.shortcuts import render

from .models import Item
from .scraping import verifyItemsToScraping


def itemsList(request):
    verifyItemsToScraping()

    items = Item.objects.all().order_by(
        'price')

    context = {'items': items}

    return render(request, 'items/list.html', context)
