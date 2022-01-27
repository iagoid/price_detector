from item.models import Item
from django.contrib import admin

# Permite a migração de dados
admin.site.register(Item)