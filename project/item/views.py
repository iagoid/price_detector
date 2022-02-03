from email import message
import multiprocessing
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from item.forms import ItemForm
import urllib.request
from bs4 import BeautifulSoup

from .models import Item
from .scraping import getSite, repeaterItemsToScraping, verifyItemsToScraping, verifySite
from multiprocessing import Process

p =  multiprocessing.Process(target= repeaterItemsToScraping)
p.start()

def itemsList(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)

        if form.is_valid():
            item = form.save(commit = False)
            try: 
                page = urllib.request.urlopen(item.link)
                soup = BeautifulSoup(page, 'html5lib')
                verifySite(soup, item)
                messages.success(request, 'Criado com sucesso.')

                return redirect('/')

            except:
                messages.error(request, 'A url inválida' + item.link)
                return redirect('/')

    else :
        items = Item.objects.exclude(price=0).order_by('price')
        unavailableItems  = Item.objects.filter(price=0)

        form = ItemForm

        context = {
            'items': items,
            'unavailableItems': unavailableItems,
            'form': form,
            }

        return render(request, 'items/list.html', context)


def deleteItem(request, id):
    task = get_object_or_404(Item, pk=id)
    task.delete()

    messages.success(request, 'Deletado com sucesso.')
    return redirect('/')