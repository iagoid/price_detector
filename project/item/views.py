from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from item.forms import ItemForm

from .models import Item
from .scraping import verifyItemsToScraping
from multiprocessing import Process


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


def deleteItem(request, id):
    task = get_object_or_404(Item, pk=id)
    task.delete()

    messages.info(request, 'Tarefa deletada com sucesso.')

    return redirect('/')