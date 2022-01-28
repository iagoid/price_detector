import schedule
from django.shortcuts import redirect, render

from item.forms import ItemForm

from .models import Item
from .scraping import verifyItemsToScraping


def itemsList(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)

        if form.is_valid():
            task = form.save(commit = False)
            task.save()
            return redirect('/') 

    else :
        verifyItemsToScraping()

        items = Item.objects.exclude(price=0).order_by('price')
        unavailableItems  = Item.objects.filter(price=0)

        form = ItemForm

        context = {
            'items': items,
            'unavailableItems': unavailableItems,
            'form': form,
            }

        return render(request, 'items/list.html', context)
