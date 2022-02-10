import multiprocessing
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from item.forms import ItemForm
from .models import Item
from .scraping import  repeaterItemsToScraping, sendRequestToSite, verifySite

p =  multiprocessing.Process(target= repeaterItemsToScraping)
p.start()

def itemsList(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)

        if form.is_valid():
            item = form.save(commit = False)
            try: 
                soup = sendRequestToSite(item.link)
            except:
                messages.error(request, 'Erro ao enviar requisição')
                return redirect('/')    
            
            try:
                item = verifySite(soup, item)
                
                if item.price != None:
                    item.save()
                    messages.success(request, 'Criado com sucesso.')
                    
                else:
                    messages.error(request, 'Erro ao coletar dados')
                    
                return redirect('/')

            except:
                messages.error(request, 'Loja desconhecida')
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